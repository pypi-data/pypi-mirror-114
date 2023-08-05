# pybetaface

Python libary for using the BetaFace API.

To install do 

```pip install pybetaface```

# Example Usage
```python
# Import the Libary
from pybetaface import FaceData

# Initialise FaceData
f = FaceData()

# Upload the file with the default API Key
data = f.uploadFile("https://www.williamd47.net/betaface/man.jpg", key="d45fd466-51e2-4701-8da8-04351c872236")

# Print the output
print(data)

```

