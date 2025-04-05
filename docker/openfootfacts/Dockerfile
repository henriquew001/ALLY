# Use the official MongoDB image as a base
FROM mongo:latest

# Mount the dump directory at runtime
# The dump directory should be on the host machine
# and will be mounted to /dump inside the container

# Set the entrypoint to restore the dump and then start MongoDB
ENTRYPOINT [ "/bin/bash", "-c" ]
CMD [ \
    "mongorestore /dump && ", \
    "mongod --quiet --bind_ip_all --port 27017" \
]

# Expose the MongoDB port
EXPOSE 27017