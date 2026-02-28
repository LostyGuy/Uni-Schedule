#----Python Setup----
FROM python:3.14.0
COPY backend/ app/backend
COPY /requirements.txt ./
RUN pip install -r requirements.txt

#----Launch Server----
CMD [ "uvicorn", "app.backend.core_logic:app", "--host", "127.0.0.1", "--port", "8000" ]

#! IN PROGRESS
