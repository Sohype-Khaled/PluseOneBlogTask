## Deployment Instructions

### Create Repo Secrets

in project secrets add

- **GH_PAT**: a personal github token with permissions `repo`, `workflows` and `package`.
- **GH_PAT_USER**: your github username.
- **PRODUCTION_HOST**: Production host IP
- **PRODUCTION_USER**: Production host user
- **PRODUCTION_KEY**: Production host ssh private key
  - **From appleboy/ssh-action**:
    - **Setting up a SSH Key**: Make sure to follow the below steps while creating SSH Keys and using them.
      The best practice is create the SSH Keys on local machine not remote machine. Login with username specified in
      Github Secrets. Generate a RSA Key-Pair:
    - **Generate rsa key**
      ```
      ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
      ```
    - **Add rsa key into Authorized keys**
      ```
      cat .ssh/id_rsa.pub | ssh b@B 'cat >> .ssh/authorized_keys'
      ```
    - **Copy rsa Private key**
      ```
      clip < ~/.ssh/id_rsa
      ```
    - **Save the private key to  `PRODUCTION_KEY` secret in the blog project**

### Server

- Clone the [server application](https://) repo to the production server
- Setup postgres and allow remote connection
- copy `~/path-to-project/.env.example` to `.env` and setup the environment variables



  
    

