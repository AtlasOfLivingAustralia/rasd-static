# RASD static site and assets

This component contains the infrastructure and code to launch and develop the RASD static site.

## Architecture

The RASD static site consists of a number of components:
- A private S3 bucket with bucket policy to store the static site assets
- A CloudFront distribution with cache policy to serve the site
- A CloudFront function to rewrite the URL to the index.html file
- Domain names registered in Route53 for the base location ( rasd.org.au ) and subdomains ( www.rasd.org.au )

and

- A CodePipeline with associated resources to build and deploy the site

The RASD frame work site is completely static, all assets are stored in an S3 bucket. The bucket is not publicly accessible and is configured to only take requests from the CloudFront distribution. The CloudFront distribution is https only, any http requests will be redirected. It uses the S3 bucket as an origin. There is a CloudFront function that rewrites any urls without a file name to use the index.html file. The distribution supports http2, it uses the common ACM certificate in the account that it's launched in, the ARN for that is specified in the config file. The certificate is in the us-east-1 region as required by CloudFront

![Service Architecture](architecture.png)
