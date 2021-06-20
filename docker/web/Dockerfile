# Pull base image
FROM node:15.5.1 as web

# Set work directory
WORKDIR .

# Install dependencies
COPY ./package.json .
RUN npm install

# Copy project
COPY . .

# Settings
ARG PROTOCOL
ARG HOST
ARG PORT
ARG NAME
ARG MAIL
ARG PHONE
ARG SOCIAL
ARG GOOGLE_MAP_KEY
ARG GOOGLE_MAP_LAT
ARG GOOGLE_MAP_LNG
ARG GOOGLE_MAP_ZOOM
RUN rm -f src/sets.json src/keys.json
RUN echo '{ \n\
    "server": "'$PROTOCOL'://'$HOST':'$PORT'/api/", \n\
    "sockets": "'$PROTOCOL'://'$HOST':'$PORT'/", \n\
    "name": "'$NAME'", \n\
    "mail": "'$MAIL'", \n\
    "phone": "'$PHONE'", \n\
    "social": '$SOCIAL', \n\
    "maps": { \n\
        "center": { \n\
            "lat": '$GOOGLE_MAP_LAT', \n\
            "lng": '$GOOGLE_MAP_LNG' \n\
        }, \n\
        "zoom": '$GOOGLE_MAP_ZOOM' \n\
    } \n\
} \n\
' >> src/sets.json
RUN echo '{ \n\
    "maps": { \n\
        "key": "'$GOOGLE_MAP_KEY'" \n\
    } \n\
} \n\
' >> src/keys.json

# Run
CMD npm start
