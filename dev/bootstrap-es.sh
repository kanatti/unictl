 #!/bin/bash

 # Elasticsearch URL
 ES_URL="http://localhost:9200"

 # Function to check if Elasticsearch is running
 check_elasticsearch() {
     curl -s "$ES_URL/_cluster/health" > /dev/null
     if [ $? -ne 0 ]; then
         echo "Elasticsearch is not running. Please start it and try again."
         exit 1
     fi
 }

 # Function to delete an index if it exists
 delete_index() {
     local index_name=$1
     echo "Deleting index $index_name if it exists..."
     curl -X DELETE "$ES_URL/$index_name"
     echo
 }

 # Function to create an index with mapping
 create_index() {
     local index_name=$1
     local mapping=$2
     echo "Creating index $index_name..."
     curl -X PUT "$ES_URL/$index_name" -H 'Content-Type: application/json' -d "$mapping"
     echo
 }

 # Function to index a document
 index_document() {
     local index_name=$1
     local document=$2
     curl -X POST "$ES_URL/$index_name/doc" -H 'Content-Type: application/json' -d "$document"
     echo
 }

 # Check if Elasticsearch is running
 check_elasticsearch

 # Delete and recreate users index
 delete_index "users"
 create_index "users" '{
   "mappings": {
     "doc": {
       "properties": {
         "name": { "type": "text" },
         "age": { "type": "integer" },
         "email": { "type": "keyword" }
       }
     }
   }
 }'

 # Delete and recreate products index
 delete_index "products"
 create_index "products" '{
   "mappings": {
     "doc": {
       "properties": {
         "name": { "type": "text" },
         "price": { "type": "float" },
         "category": { "type": "keyword" }
       }
     }
   }
 }'

 # Delete and recreate orders index
 delete_index "orders"
 create_index "orders" '{
   "mappings": {
     "doc": {
       "properties": {
         "order_id": { "type": "keyword" },
         "user_id": { "type": "keyword" },
         "total_amount": { "type": "float" },
         "order_date": { "type": "date" }
       }
     }
   }
 }'

 # Populate users index
 echo "Populating users index..."
 index_document "users" '{"name": "John Doe", "age": 30, "email": "john@example.com"}'
 index_document "users" '{"name": "Jane Smith", "age": 25, "email": "jane@example.com"}'

 # Populate products index
 echo "Populating products index..."
 index_document "products" '{"name": "Laptop", "price": 999.99, "category": "Electronics"}'
 index_document "products" '{"name": "Book", "price": 19.99, "category": "Books"}'

 # Populate orders index
 echo "Populating orders index..."
 index_document "orders" '{"order_id": "ORD001", "user_id": "john@example.com", "total_amount": 999.99, "order_date": "2023-06-15"}'
 index_document "orders" '{"order_id": "ORD002", "user_id": "jane@example.com", "total_amount": 19.99, "order_date": "2023-06-16"}'

 echo "Script completed. Indices created and populated with sample data."