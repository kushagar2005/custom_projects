FROM python:3.8-slim-buster
workdir /src
RUN pip install pandas
copy /src/my_script.py ./ 
CMD [ "python", "./my_script.py" ] 
