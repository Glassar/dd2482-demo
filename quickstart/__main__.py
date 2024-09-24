"""Fast and Loose Inc: Resource management"""

import pulumi
from pulumi_gcp import storage

# Create a GCP resource (Storage Bucket)
userData = storage.Bucket('my-bucket', location="US")

binding = storage.BucketIAMBinding ("member", 
 bucket= bucket.name,
 members= ["allUsers"],
 role= "roles/storage.objectViewer",
)

# Export the DNS name of the bucket
pulumi.export('bucket_name', bucket.url)
