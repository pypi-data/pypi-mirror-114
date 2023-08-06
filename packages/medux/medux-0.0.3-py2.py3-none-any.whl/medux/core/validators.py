from django.core.validators import RegexValidator

fhir_server_allowed_references = "Account|ActivityDefinition|AdverseEvent|AllergyIntolerance|Appointment|" \
        "AppointmentResponse|AuditEvent|Basic|Binary|BiologicallyDerivedProduct|" \
        "BodyStructure|Bundle|CapabilityStatement|CarePlan|CareTeam|ChargeItem|Claim|" \
        "ClaimResponse|ClinicalImpression|CodeSystem|Communication|CommunicationRequest|" \
        "CompartmentDefinition|Composition|ConceptMap|Condition|Consent|Contract|" \
        "Coverage|DetectedIssue|Device|DeviceComponent|DeviceMetric|DeviceRequest|" \
        "DeviceUseStatement|DiagnosticReport|DocumentManifest|DocumentReference|" \
        "EligibilityRequest|EligibilityResponse|Encounter|Endpoint|EnrollmentRequest|" \
        "EnrollmentResponse|EntryDefinition|EpisodeOfCare|EventDefinition|" \
        "ExampleScenario|ExpansionProfile|ExplanationOfBenefit|FamilyMemberHistory|Flag|" \
        "Goal|GraphDefinition|Group|GuidanceResponse|HealthcareService|ImagingStudy|" \
        "Immunization|ImmunizationEvaluation|ImmunizationRecommendation|" \
        "ImplementationGuide|Invoice|ItemInstance|Library|Linkage|List|Location|" \
        "Measure|MeasureReport|Media|Medication|MedicationAdministration|" \
        "MedicationDispense|MedicationRequest|MedicationStatement|MedicinalProduct|" \
        "MedicinalProductAuthorization|MedicinalProductClinicals|" \
        "MedicinalProductDeviceSpec|MedicinalProductIngredient|" \
        "MedicinalProductPackaged|MedicinalProductPharmaceutical|MessageDefinition|" \
        "MessageHeader|NamingSystem|NutritionOrder|Observation|" \
        "ObservationDefinition|OccupationalData|OperationDefinition|" \
        "OperationOutcome|Organization|OrganizationRole|Patient|PaymentNotice|" \
        "PaymentReconciliation|Person|PlanDefinition|Practitioner|" \
        "PractitionerRole|Procedure|ProcessRequest|ProcessResponse|" \
        "ProductPlan|Provenance|Questionnaire|QuestionnaireResponse|" \
        "Relationship|RequestGroup|ResearchStudy|ResearchSubject|" \
        "RiskAssessment|Schedule|SearchParameter|Sequence|" \
        "ServiceRequest|Slot|Specimen|SpecimenDefinition|StructureDefinition|" \
        "StructureMap|Subscription|Substance|SubstancePolymer|" \
        "SubstanceReferenceInformation|SubstanceSpecification|SupplyDelivery|" \
        "SupplyRequest|Task|TerminologyCapabilities|TestReport|TestScript|" \
        "UserSession|ValueSet|VerificationResult|VisionPrescription" + "|Any"


CodeValidator = RegexValidator(regex=r'[^\s]+([\s]?[^\s]+)*',
                               message='A Code must not contain whitespaces.')

IdValidator = RegexValidator(regex=r'[a-z][A-Z][0-9][-.]?',
                             message='Ids can be up to 64 characters long, '
                                     'and contain any combination of upper '
                                     'and lowercase ASCII letters, numerals,'
                                     ' "-" and "."')

OidValidator = RegexValidator(r'[0-2](\.[1-9]\d*)+',
                              message='Given string is no OID')


