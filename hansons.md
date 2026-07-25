


<img width="1024" height="209" alt="image" src="https://github.com/user-attachments/assets/9b7302a9-fab1-4a36-b526-b0eb6b7652d4" />


<img width="1884" height="857" alt="image" src="https://github.com/user-attachments/assets/39943a32-87ca-4ec3-87ff-e2e2e000a6ba" />


<img width="962" height="329" alt="image" src="https://github.com/user-attachments/assets/df30c72e-3db6-46aa-b477-08c5a307b8fd" />



TOKEN=$(curl -s -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600") && curl -s -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/instance-type
