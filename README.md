## API Documentation

### Endpoint: `/api/categories/`
#### Request
- **Method:** GET
- **Permissions:** Public (AllowAny)
- **Query Parameters:**
  - search: string (optional)

#### Response

- **Status Code:** 200 OK
- **Content Type:** `application/json`

#### Sample Response Body

```json
[
  {
    "id": 1,
    "name": "Category 1",
    "slug": "category-1"
  },
  {
    "id": 2,
    "name": "Category 2",
    "slug": "category-2"
  }
]
```

### Endpoint: `/api/tags/`
#### Request

- **Method:** GET
- **Permissions:** Public (AllowAny)
- **Query Parameters:**
    - search: string (optional)

#### Response

- **Status Code:** 200 OK
- **Content Type:** `application/json`

#### Sample Response Body

```json
[
  {
    "id": 1,
    "name": "Tag 1",
    "slug": "tag-1"
  },
  {
    "id": 2,
    "name": "Tag 2",
    "slug": "tag-2"
  }
]
```

### Endpoint: `/api/posts/`
#### Request


## Deployment Instructions

### Setting Up Repository Secrets

To configure secrets for your project, follow these steps:

- **GH_PAT**: Personal GitHub token with permissions for `repo`, `workflows`, and `package`.
- **GH_PAT_USER**: Your GitHub username.
- **PRODUCTION_HOST**: IP address of the production host.
- **PRODUCTION_USER**: Username for accessing the production host.
- **PRODUCTION_KEY**: SSH private key for accessing the production host.

#### Using SSH Key from appleboy/ssh-action:

When setting up SSH keys, follow these guidelines:

1. **Generate RSA Key Pair**: Create the RSA key pair on your local machine:

  ```bash
  ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
  ```

2. **Add RSA Key to Authorized Keys**: Ensure the public key is added to the authorized keys on the production server:

  ```bash
  cat ~/.ssh/id_rsa.pub | ssh PRODUCTION_USER@PRODUCTION_HOST 'cat >> ~/.ssh/authorized_keys'
  ```

3. **Save Private Key**: Copy the private key to your clipboard:

```bash
clip < ~/.ssh/id_rsa
```

4. **Store Private Key**: Save the private key as the value for the `PRODUCTION_KEY` secret in your project secrets.

### Deploying Server Application

To deploy the server application to the production server:

- Clone the [server application repository](https://github.com/Sohype-Khaled/PlusOneBlogTaskServer) onto the production
  server.
- Follow the installation instructions provided in the server application's documentation.

