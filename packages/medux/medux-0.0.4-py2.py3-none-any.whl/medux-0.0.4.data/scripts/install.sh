#!/bin/sh

export REPO="https://gitlab.com/nerdocs/medux/medux.git"
export MEDUX_USER=medux
export DATABASE_ENGINE=postgresql

# =================================================================
export USE_GIT=0

# =========  subprocedures  =========

die() {
  if [ "$1" != "" ]; then
    echo "ERROR: $1"
  fi
  exit 1
}

render() {
  eval "echo \"$(cat $1)\""
}

try_import() {
  export ${1}="$()"
}

usage() {
  cat << EOF

Usage: $(basename $0) [ -h ] [ -g | --git ]

Options:
    -h        Show usage
    -g        use newest git commit instead of installing the PyPi version
EOF

}
# ========= COMMON part ==========
PARSED_ARGUMENTS=$(getopt -o hg --long git,as-user -- "$@")
VALID_ARGUMENTS=$?
if [ "$VALID_ARGUMENTS" != "0" ]; then
  usage
  exit 2
fi

eval set -- "$PARSED_ARGUMENTS"
while true; do
  case "$1" in
    -g | --git)
      USE_GIT=1
      shift
      ;;
    -h | --help)
      usage;
      exit 2
      ;;
    --as-user)
      # undocumented, used for calling this script as normal user
      shift
      break
      ;;
    --)
      shift
      break
      ;;
    # If invalid options were passed, then getopt should have reported an error,
    # which we checked as VALID_ARGUMENTS when getopt was called...
    *) echo "Unexpected option: $1 - this should not happen."
       usage ;;
  esac
done

# =========  ROOT USER part  =========

if [ "$(whoami)" = "root" ]; then
  if [ -f medux/.env ]; then
    # trying to read SECRET_KEY and DB_PASSWORD from existing .env file"
    SECRET_KEY=$(grep SECRET_KEY medux/.env | cut -d= -f2)
    export SECRET_KEY
    DB_PASSWORD=$(grep DATABASE_PASS medux/.env | cut -d= -f2)
    export DB_PASSWORD
  fi

  if [ "${SECRET_KEY}" != "" ]; then
      echo "Using Django's SECRET_KEY from env."
  else
    SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe())")
    echo "SECRET_KEY=${SECRET_KEY}"
    export SECRET_KEY
  fi

  if [ "${DB_PASSWORD}" != "" ]; then
    echo "Using DB_PASSWORD from env."
  else
    DB_PASSWORD=$(python3 -c "import secrets; print(secrets.token_urlsafe())")
    export DB_PASSWORD
    echo "DB_PASSWORD=${DB_PASSWORD}"
  fi

  if [ "${DOMAIN}" = "" ]; then
    while [ "${DOMAIN}" = "" ]; do
      echo -n "Please enter domain name for server: "
      read DOMAIN
    done
  else
    echo "Using domain name from env variable DOMAIN: ${DOMAIN}."
  fi
  # TODO: validate DOMAIN name

  echo "\nInstalling necessary software..."
  apt-get install -y python3 python3-pip python3-virtualenv nginx uwsgi postgresql >/dev/null
  test ${USE_GIT} = 1 && apt-get install git > /dev/null

  # mariadb-server mariadb-client python3-dev default-libmysqlclient-dev build-essential

  useradd --create-home --system --user-group --shell /bin/bash ${MEDUX_USER} >/dev/null 2>&1

  cd /var/www || die "/var/www directory not found"
  mkdir -p medux || die "Could not create medux directory"
  chown ${MEDUX_USER}:${MEDUX_USER} medux
  cd medux || die "Error entering medux directory (permissions?)"

  # call this script again, but as MEDUX_USER, do user specific tasks there (see below)
  echo "Switching to '${MEDUX_USER}' user..."
  # TODO: maybe find a better way to preserve environment variables... (sudo -E ?)

## debug
#  echo "checking variables as root..."
#  echo "REPO: ${REPO}"
#  echo "MEDUX_USER: ${MEDUX_USER}"
#  echo "SECRET_KEY: ${SECRET_KEY}"
#  echo "DB_PASSWORD: ${DB_PASSWORD}"

  echo "Switching to medux user..."
  export ALLOW_AS_USER=1
  sudo --preserve-env --set-home -u ${MEDUX_USER} $0 --as-user || die
  unset ALLOW_AS_USER
  # then continue with root tasks...
  echo "Continuing as root user..."

  # install startup files
  render setup/medux_nginx.conf.tpl | tee /etc/nginx/sites-available/medux.conf >/dev/null
  render setup/medux.service.tpl | tee /etc/systemd/system/medux.service >/dev/null

  # setup PostGreSQL database
  cd /tmp || die "Could not cd into /tmp"
  sudo -u postgres psql -c "create database medux;"
  sudo -u postgres psql -c "create user ${MEDUX_USER} with encrypted password '${DB_PASSWORD}';"
  sudo -u postgres psql -c "grant all privileges on database medux to ${MEDUX_USER};"

  # enable nginx/medux services
  ln -sf /etc/nginx/sites-available/medux.conf /etc/nginx/sites-enabled/
  systemctl enable medux.service
  systemctl enable nginx.service
  systemctl restart medux.service
  systemctl restart nginx.service

  # ==================== Finally... =========================
  echo "Installation finished."
  echo " * Please keep the PostgreSQL database password in a safe place: ${DB_PASSWORD}"

# =========  MEDUX_USER part  =========
elif [ "$(whoami)" = "${MEDUX_USER}" ]; then


  if [ "${ALLOW_AS_USER}" != "1" ]; then
    # "secret" internal switch not triggered...
    die "Please run this script as root user."
  fi

  cd /var/www/medux || die "var/www/medux is not accessible."
  if [ ${USE_GIT} = 1 ]; then
    if [ -d .git ]; then
      echo "Found already installed git repository. Updating..."
      git pull
    else
      git clone ${REPO} . --depth=1 || die "Error cloning medux repository: ${REPO}." >/dev/null
    fi
  fi
  if [ ! -d .venv ]; then
    echo "Creating virtualenv..."
    virtualenv .venv >/dev/null
  fi

  . .venv/bin/activate
  grep -q "venv/bin/activate" ~/.bashrc || echo ". /var/www/medux/.venv/bin/activate" >> ~/.bashrc

  pip install --upgrade pip
  # FIXME: install medux locally - this is required as long as medux is not available in pypi
  if [ ${USE_GIT} = 1 ]; then
    pip install -e . || die "Could not install medux from local repository."
    pip install -r requirements/prod.txt || die "Could not install medux dependencies."
  else
    pip install medux || die "Could not install medux from PyPi."
  fi
  ./manage.py collectstatic --noinput
  ./manage.py migrate

  render setup/.env.example > medux/.env
fi
