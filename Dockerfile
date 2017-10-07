FROM python:3

# Set the application directory
WORKDIR /semantics

# Install our requirements.txt
ADD requirements.txt /semantics/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m spacy download en_core_web_sm

# Copy our code from the current folder to /app inside the container
ADD . /semantics

# Define our command to be run when launching the container
CMD ["python", "app.py"]