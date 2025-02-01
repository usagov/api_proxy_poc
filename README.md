# API Proxy for Cloud.gov

## 📌 Overview

This project is a **Flask-based API Proxy** designed to securely **relay API requests** while **hiding API credentials** from users. It enables a **test client** to send API queries via the proxy, ensuring credentials remain **server-side only**.

The **proxy application** intercepts API calls and appends the required API key **before forwarding requests** to the external API (e.g., `SAM.gov`). It is deployed using **Cloud Foundry** on **Cloud.gov**.

## 🏗️ Architecture

```
┌───────────────┐        ┌───────────────┐        ┌─────────────────┐
│ Test Client   │  --->  │ API Proxy     │  --->  │ External API    │
│ (requests)    │        │ (forwards)    │        │ (e.g., SAM.gov) │
└───────────────┘        └───────────────┘        └─────────────────┘
```

- **Test Client**: Makes API requests but **lacks direct API credentials**.
- **API Proxy**: Relays requests, appends `API_KEY`, and forwards them securely.
- **External API**: The **actual API** (e.g., `SAM.gov`) that receives requests.

## 🚀 Deployment

### **1️⃣ Prerequisites**

- Cloud Foundry CLI (`cf`) installed
- Access to **Cloud.gov** environment
- A Cloud.gov **org & space targeted** (`cf login && cf target`)
- Environment variables:
  - `API_ENDPOINT` (Base API URL)
  - `API_KEY` (Secret API Key)

### **2️⃣ Setup**

Set environment variables:

```bash
export API_ENDPOINT="https://api.sam.gov/opportunities/v2/search"
export API_KEY="your-secret-key"
```

### **3️⃣ Deploy**

To deploy the API Proxy & Test Client, run:

```bash
./deploy.sh
```

- The script will confirm **your Cloud Foundry org & space** before proceeding.
- It **creates routes**, **deploys applications**, and **sets network policies**.
- The expected output:
  ```plaintext
  ✅ Configuration prepared
  🔄 Checking routes...
  ✅ All required routes already exist.
  🚀 Deploying API Proxy...
  ✅ API Proxy deployed successfully.
  🚀 Deploying Test Client...
  ✅ Test Client deployed successfully.
  🔒 Configuring network policies...
  ✅ Network policies added.
  ✅ Cleanup complete.
  🎉 Deployment completed successfully!
  ```

## 🔧 Usage

### **1️⃣ Make a request from the Test Client**

```bash
cf ssh test-client
curl -v "https://api-proxy.apps.internal:61443/proxy?postedFrom=01/01/2024&postedTo=01/31/2024"
```

This request:

- Routes through `api-proxy.apps.internal`
- Appends `API_KEY`
- Sends the request to `SAM.gov`

## 🌎 Environment Variables

| Variable       | Description        | Example Value                                 |
| -------------- | ------------------ | --------------------------------------------- |
| `API_ENDPOINT` | The base API URL   | `https://api.sam.gov/opportunities/v2/search` |
| `API_KEY`      | The secret API key | `your-secret-key`                             |

## 🛠️ Troubleshooting

### **❌ `API_KEY` Not Found**

Check that `API_KEY` is set:

```bash
echo $API_KEY
```

If empty, export it:

```bash
export API_KEY="your-secret-key"
```

### **❌ Cloud Foundry Org/Space Not Set**

Run:

```bash
cf target
```

Ensure it matches the expected **org & space**.

### **❌ Deployment Fails**

Try redeploying:

```bash
cf push -f api_proxy_manifest.yml
cf push -f test_client_manifest.yml
```

### **❌ Proxy Returns 404**

- Confirm the request URL is correct.
- Ensure `api-proxy` is running:
  ```bash
  cf apps
  ```

## 📌 Future Enhancements

- [ ] **Add authentication** to restrict access to `api-proxy`
- [ ] **Enable logging aggregation** for API requests
- [ ] **Support multiple external APIs** dynamically
