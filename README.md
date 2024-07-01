# Plus One Blog Task

- [Admin Panel](http://ec2-18-169-216-27.eu-west-2.compute.amazonaws.com/admin/)
- [Swagger API Documentation](http://ec2-18-169-216-27.eu-west-2.compute.amazonaws.com/api/swagger/)
- [server application repository](https://github.com/Sohype-Khaled/PlusOneBlogTaskServer)

## Setup Instructions
### Prerequisites
- Python 3.10+
- pip (Python package installer)
- virtualenv (recommended for virtual environment management)
- PostgreSQL (if using PostgreSQL as the database)

#### Step 1: Clone the Repository
```shell
git clone https://github.com/Sohype-Khaled/PluseOneBlogTask.git
cd PluseOneBlogTask
```
#### Step 2: Set Up a Virtual Environment
It's recommended to use a virtual environment to manage your project dependencies.
```shell
python3 -m venv venv
source venv/bin/activate 
```

#### Step 3: Install Dependencies
Install the required Python packages using pip.
```shell
pip install -r requirements.txt
```
#### Step 4: Copy `.env.example` tot `.env` and configure the file


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

- **Method:** GET
- **Permissions:** Public (AllowAny)
- **Query Parameters:**
    - q: (string) Search term for filtering posts by title or content (optional)
    - categories: (string) Filter posts by category IDs (comma-separated) (optional)
    - tags: (string) Filter posts by tag IDs (comma-separated) (optional)
    - limit: (integer) Limit the posts results (optional)
    - offset: (integer) The starting offset of results (optional)

#### Response

- **Status Code:** 200 OK
- **Content Type:** `application/json`

#### Sample Request Data

```json
{
  "count": 52,
  "next": "http://localhost:8000/api/posts/?limit=20&offset=20",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Bit past pass movie alone.",
      "content": "Simple technology camera read. Around particular necessary for before plan. Space TV someone program.",
      "author": {
        "id": 2,
        "bio": null,
        "profile_picture": null,
        "user": {
          "id": 2,
          "first_name": "Luis",
          "last_name": "Young",
          "username": "luisyoung",
          "email": "ayalajoseph@example.org"
        }
      },
      "categories": [],
      "tags": [],
      "created_at": "2024-06-30T20:48:26.506278Z",
      "updated_at": "2024-06-30T20:48:26.579153Z"
    }
  ]
}
```

### Endpoint: `/api/posts/`

#### Request

- **Method:** POST
- **Permissions:** Private (IsAuthenticated)
- **Request Data:**
    - title: String
    - content: String
    - categories: list of category IDs
    - tags: list of tag IDs

#### Sample Request Data

```json
{
  "title": "Blog Post 1",
  "content": "Blog Post 1 Content",
  "categories": [
    3
  ],
  "tags": [
    1,
    2
  ]
}
```

#### Response

- **Status Code:** 201 Created
- **Content Type:** `application/json`

#### Sample Response Body

```json
{
  "id": 52,
  "title": "Blog Post 1",
  "content": "Blog Post 1 Content",
  "author": {
    "id": 1,
    "bio": null,
    "profile_picture": null,
    "user": {
      "id": 1,
      "first_name": "",
      "last_name": "",
      "username": "sohype",
      "email": "sohype@mail.com"
    }
  },
  "categories": [
    {
      "id": 3,
      "name": "Electronics",
      "slug": "electro"
    }
  ],
  "tags": [
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
  ],
  "created_at": "2024-06-30T22:21:17.237901Z",
  "updated_at": "2024-06-30T22:21:17.237930Z"
}
```

### Endpoint: `/api/posts/:id/`

#### Request

- **Method:** GET
- **Permissions:** Public (AllowAny)

#### Response

- **Status Code:** 200 Ok
- **Content Type:** `application/json`

#### Sample Response Body

```json
{
  "id": 52,
  "title": "Blog Post 1",
  "content": "Blog Post 1 Content",
  "author": {
    "id": 1,
    "bio": null,
    "profile_picture": null,
    "user": {
      "id": 1,
      "first_name": "",
      "last_name": "",
      "username": "sohype",
      "email": "sohype@mail.com"
    }
  },
  "categories": [
    {
      "id": 3,
      "name": "Electronics",
      "slug": "electro"
    }
  ],
  "tags": [
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
  ],
  "created_at": "2024-06-30T22:21:17.237901Z",
  "updated_at": "2024-06-30T22:21:17.237930Z"
}
```

### Endpoint: `/api/posts/:id/`

#### Request

- **Method:** PUT
- **Permissions:** Private (IsAuthenticated)
- **Request Data:**
    - title: String
    - content: String
    - categories: list of category IDs
    - tags: list of tag IDs

#### Sample Request Data

```json
{
  "title": "Blog Post 1",
  "content": "Blog Post 1 Content",
  "categories": [
    3
  ],
  "tags": [
    1,
    2
  ]
}
```

#### Response

- **Status Code:** 200 OK
- **Content Type:** `application/json`

#### Sample Response Body

```json
{
  "id": 52,
  "title": "Blog Post 1",
  "content": "Blog Post 1 Content",
  "author": {
    "id": 1,
    "bio": null,
    "profile_picture": null,
    "user": {
      "id": 1,
      "first_name": "",
      "last_name": "",
      "username": "sohype",
      "email": "sohype@mail.com"
    }
  },
  "categories": [
    {
      "id": 3,
      "name": "Electronics",
      "slug": "electro"
    }
  ],
  "tags": [
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
  ],
  "created_at": "2024-06-30T22:21:17.237901Z",
  "updated_at": "2024-06-30T22:21:17.237930Z"
}
```

### Endpoint: `/api/posts/:id/`

#### Request

- **Method:** DELETE
- **Permissions:** Private (IsAuthenticated)

#### Response

- **Status Code:** 204 No Content
- **Content Type:** `application/json`

### Endpoint: `/api/comments/`

#### Request

- **Method:** GET
- **Permissions:** Public (AllowAny)
- **Query Parameters:**
    - q: (string) Search term for filtering comment by content (optional)
    - post: (string) Filter comment by posts IDs (comma-separated) (optional)
    - author: (string) Filter comments by authors IDs (comma-separated) (optional)

#### Response

- **Status Code:** 200 OK
- **Content Type:** `application/json`

#### Sample Request Data

```json
[
  {
    "id": 1,
    "post": 1,
    "content": "This Post is awesome",
    "author": {
      "id": 1,
      "bio": null,
      "profile_picture": null,
      "user": {
        "id": 1,
        "first_name": "Sohype",
        "last_name": "Khaled",
        "username": "sohype",
        "email": "sohype@mail.com"
      }
    },
    "created_at": "2024-06-30T23:45:31.497706Z"
  }
]
```

### Endpoint: `/api/comments/`

#### Request

- **Method:** POST
- **Permissions:** Private (IsAuthenticated)
- **Request Data:**
    - post: Integer
    - content: String

#### Sample Request Data

```json
{
  "post": 1,
  "content": "This Post is awesome"
}
```

#### Response

- **Status Code:** 201 Created
- **Content Type:** `application/json`

#### Sample Response Body

```json
{
  "id": 1,
  "post": 1,
  "content": "This Post is awesome",
  "author": {
    "id": 1,
    "bio": null,
    "profile_picture": null,
    "user": {
      "id": 1,
      "first_name": "Sohype",
      "last_name": "Khaled",
      "username": "sohype",
      "email": "sohype@mail.com"
    }
  },
  "created_at": "2024-06-30T23:45:31.497706Z"
}
```

### Endpoint: `/api/comments/:id/`

#### Request

- **Method:** DELETE
- **Permissions:** Private (IsAuthenticated)

#### Response

- **Status Code:** 204 No Content
- **Content Type:** `application/json`

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

  ```shell
  ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
  ```

2. **Add RSA Key to Authorized Keys**: Ensure the public key is added to the authorized keys on the production server:

  ```shell
  cat ~/.ssh/id_rsa.pub | ssh PRODUCTION_USER@PRODUCTION_HOST 'cat >> ~/.ssh/authorized_keys'
  ```

3. **Save Private Key**: Copy the private key to your clipboard:

```shell
clip < ~/.ssh/id_rsa
```

4. **Store Private Key**: Save the private key as the value for the `PRODUCTION_KEY` secret in your project secrets.

### Deploying Server Application

To deploy the server application to the production server:

- Clone the [server application repository](https://github.com/Sohype-Khaled/PlusOneBlogTaskServer) onto the production
  server.
- Follow the installation instructions provided in the server application's documentation.

