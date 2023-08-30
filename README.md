# Flask Mobile Factory API

Welcome to the Flask Mobile Factory API project! This API allows you to create orders for configurable mobiles. The code for this project can be found in the following repository.

https://github.com/Ritesh7766/MobileFactory

## Setting Up and Running the Application

### Creating a Virtual Environment

#### Windows

1. Open a command prompt.

2. Navigate to your project directory using the `cd` command:

&emsp;&emsp;cd path/to/the/project

3. Create a virtual environment named "env":

&emsp;&emsp;python3 -m venv env

4. Activate the virtual environment:

&emsp;&emsp;.\env\Scripts\activate

#### Ubuntu

1. Open a terminal.

2. Navigate to your project directory using the `cd` command:

&emsp;&emsp;cd path/to/your/project

3. Create a virtual environment named "env":

&emsp;&emsp;python3 -m venv env

4. Activate the virtual environment:

&emsp;&emsp;source env/bin/activate

### Installing Requirements

1. With the virtual environment activated, install the project dependencies from the `requirements.txt` file:

&emsp;&emsp;pip3 install -r requirements.txt

### Running the Application

1. In the project directory, run the following command to start the Flask application:

&emsp;&emsp;flask run

2. The application will be accessible at `http://127.0.0.1:5000/` in your web browser.

3. To stop the application, press `Ctrl+C` in the terminal.

### Testing the Application

1. In the project directory, run the following command to test the Flask application:

&emsp;&emsp;python3 -m unittest discover

## API Usage

Once the application is running, you can use the following API endpoint to create orders for configurable mobiles.

- **Endpoint:** `/order`
- **Method:** POST
- **Payload:** JSON object with `components` field containing a list of component codes.

**Example payload:**

```json
{
    "components": ["I", "A", "D", "F", "K"]
}
```

**Response:**

```json
{
    "order_id": "20230830213449_3256787356",
    "total": 142.3,
    "parts": [
        "LED Screen",
        "Wide-Angle Camera",
        "USB-C Port",
        "Android OS",
        "Metallic Body"
    ]
}
```

**Example invalid payload:**
```json
{
    "random_string": []
}
```

**Response:**
```json
{
    "message": {
        "components": "Missing required parameter in the JSON body"
    }
}
```

**Example invalid payload:**
```json
{
    "components": ["I", "A", "D", "K", "K"]
}
```

**Response:**
```json
{
    "Missing Components": [
        "Port"
    ],
    "Repeated Component Types": [
        "Body"
    ]
}
```

**Example invalid payload:**
```json
{
     "components": ["I", "A", "A", "K", "K"]
}
```

**Response:**
```json
{
    "Missing Components": [
        "Port",
        "Camera"
    ],
    "Repeated Component Types": [
        "Screen",
        "Body"
    ]
}
```

**Example invalid payload:**
```json
{
     "components": ["1", "2", "3", "4"]
}
```

**Response:**
```json
{
    "Missing Components": [
        "Port",
        "OS",
        "Screen",
        "Body",
        "Camera"
    ],
    "Invalid Codes": [
        "4",
        "3",
        "2",
        "1"
    ]
}
```
