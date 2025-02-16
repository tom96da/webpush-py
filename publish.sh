HOST=https://localhost
ID=1412
TITLE="Title of Notification"
BODY="Body of Notification"

curl -k -X POST "${HOST}/publish" -H "Content-Type: application/json" -d "{\"title\": \"${TITLE}\", \"body\": \"${BODY}\", \"id\": ${ID}}"
