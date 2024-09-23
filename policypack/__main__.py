from pulumi_policy import (
    EnforcementLevel,
    PolicyPack,
    ReportViolation,
    ResourceValidationArgs,
    ResourceValidationPolicy,
)

def storage_bucket_no_public_access_validator(args: ResourceValidationArgs, report_violation: ReportViolation):
    if args.resource_type == "gcp:storage/bucketIAMBinding:BucketIAMBinding":
        access = args.props["members"]
        role = args.props["role"]
        if "allUsers" in access:
            if role == "roles/storage.objectViewer":
                report_violation("Storage buckets has IAM policy allowing public read access for allUsers")
            elif role == "roles/storage.objectAdmin":
                report_violation("Storage buckets has IAM policy allowing public admin access for allUsers")
            elif role == "roles/storage.objectUser":
                report_violation("Storage buckets has IAM policy allowing public access to read and write for allUsers")
            else:
                report_violation("Storage buckets has IAM policy allowing public of some sort to allUsers")

storage_bucket_no_public_access = ResourceValidationPolicy(
    name="storage_bucket_no_public_access",
    description="Prohibits an IAM policy allowing for public access",
    validate=storage_bucket_no_public_access_validator,
)

PolicyPack(
    name="gcp-python",
    enforcement_level=EnforcementLevel.MANDATORY,
    policies=[
        storage_bucket_no_public_access,
    ],
)
