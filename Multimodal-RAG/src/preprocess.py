from unstructured.partition.pdf import partition_pdf
import os
from pdf2image.exceptions import PDFInfoNotInstalledError
from IPython.display import Image, display
import base64
from langchain_ollama import ChatOllama
import json
from unstructured.documents.elements import Image
import pickle
from unstructured.documents.elements import Element
# absolute path is from root of the file system
# relative path is from the current working directory

base_dir=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_path = os.path.join(base_dir,"data","attention.pdf")
if not os.path.exists(file_path):
    raise FileNotFoundError(f"File not found: {file_path}")



# chunks = partition_pdf(
#     filename=file_path,
#     infer_table_structure=True,            # extract tables
#     strategy="hi_res",                     # mandatory to infer tables

#     extract_image_block_types=["Image"],   # Add 'Table' to list to extract image of tables
#     # image_output_dir_path=output_path,   # if None, images and tables will saved in base64

#     extract_image_block_to_payload=True,   # if true, will extract base64 for API usage

#     chunking_strategy="by_title",          # or 'basic'
#     max_characters=10000,                  # defaults to 500
#     combine_text_under_n_chars=2000,       # defaults to 0
#     new_after_n_chars=6000,

#     # extract_images_in_pdf=True,          # deprecated
# )
# with open("chunks.pkl", "wb") as f:
#     pickle.dump(chunks, f)


with open("chunks.pkl", "rb") as f:
    chunks = pickle.load(f)



# elements=chunks[2].metadata.orig_elements
# chunk_images=[element for element in elements if "Image" in str(type(element))]
# chunk_images[0]

# print(chunk_images[0].to_dict())



















# with open("final_chunks.json", "r", encoding="utf-8") as f:
#     chunks = json.load(f)

# try:
#     elements = chunks[0]['metadata']['orig_elements']
#     print(type(elements))
#     print(chunks[0]['metadata'])
# except (IndexError, KeyError):
#     print("Missing keys or empty chunks.")
#     elements = []

# chunk_images = [
#     element for element in elements
#     if isinstance(element, dict) and 'Image' in str(element.get('type', ''))
# ]

# if chunk_images:
#     print(chunk_images[0])  # Already a dictionary
# else:
#     print("No image elements found.")
# elements = chunks[0]['metadata']['orig_elements']
# chunk_images = [element for element in elements if "Image" in str(element.get('type', ''))]

# print(chunk_images[0]) 
# chunk_images=[element for element in elements if "Image" in str(type(element))]
# print(chunk_images[0].to_dict())
# chunks_dicts = [chunk.to_dict() for chunk in chunks]
try:
    print(len(chunks))
except:
    pass

# serialized_chunks = [chunk.to_dict() for chunk in chunks]

# # # Save as JSON file
# with open("final_chunks.json", "w", encoding="utf-8") as f:
#     json.dump(serialized_chunks, f, ensure_ascii=False, indent=2)

tables=[]
texts=[]



for chunk in chunks:
  if "Table" in str(type(chunk)):
    tables.append(chunk)
  if "CompositeElement" in str(type((chunk))):
    texts.append(chunk)


def get_images_base64(chunks):
  images_b64=[]
  for chunk in chunks:
    if "CompositeElement" in str(type(chunk)):
      chunk_ele=chunk.metadata.orig_elements
      for ele in chunk_ele:
        if "Image" in str(type(ele)):
          images_b64.append(ele.metadata.image_base64)
  return images_b64
images=get_images_base64(chunks)


# Example: Display the first image
# image_base64 = images[0]

# Decode the base64 string
# image_data = base64.b64decode(image_base64)

# Save it as a temporary PNG file
# with open("output_image.png", "wb") as f:
#     f.write(image_data)

# print("Image saved as output_image.png")
# # Save to JSON file
# save_path = os.path.join(base_dir, "data", "chunks.json")
# with open(save_path, "w", encoding="utf-8") as f:
#     json.dump(chunks_dicts, f, ensure_ascii=False, indent=2)
# serialized_chunks = [chunk.to_dict() for chunk in chunks]

# # # Save as JSON file
# with open("my_chunks.json", "w", encoding="utf-8") as f:
#     json.dump(serialized_chunks, f, ensure_ascii=False, indent=2)



# serializable_chunks = []
# for chunk in chunks:
#     chunk_dict = chunk.to_dict()  # convert chunk object to dict
    
#     metadata = chunk_dict.get("metadata", {})
#     image_data = metadata.get("image_base64")
    
#     # If image_base64 is bytes, decode to str
#     if isinstance(image_data, bytes):
#         metadata["image_base64"] = image_data.decode("utf-8")
    
#     # If image_base64 is not present or already str, do nothing
    
#     serializable_chunks.append(chunk_dict)

# # Save to JSON
# with open("new.json", "w", encoding="utf-8") as f:
#     json.dump(serializable_chunks, f, ensure_ascii=False, indent=2)

# Save to JSON file
# with open('output.json', 'w', encoding='utf-8') as f:

# with open("new.json", "r", encoding="utf-8") as f:
#     loaded_json = json.load(f)

# elements_from_json = loaded_json[3]['metadata']['orig_elements'] # Assuming the structure is similar to your original chunks

# chunk_images_from_json = [element for element in elements_from_json if isinstance(element, dict) and element.get('type') == 'Image']

# # You can then access the first image element like this:
# if chunk_images_from_json:
#     first_image_from_json = chunk_images_from_json[0]
#     print(first_image_from_json)
#     print("success")
# else:
#     print("No image elements found in the specified chunk.")

# print(loaded_json[0])
# Step 2: Reconstruct the original chunk objects (CompositeElements)
# chunks = [Element.from_dict(chunk_dict) for chunk_dict in loaded_json]
# with open(save_path, "r", encoding="utf-8") as f:
#     loaded_dicts = json.load(f)

# Reconstruct Element objects
# loaded_chunks = [Element.from_dict(d) for d in loaded_dicts]


# save_path = os.path.join(base_dir, "data", "chunks.pkl")

# with open(save_path, "wb") as f:
#     pickle.dump(chunks, f)

# with open(save_path, "rb") as f:
#     loaded_chunks = pickle.load(f)

# elements = loaded_chunks[3].metadata.orig_elements

# chunk_images = [el for el in elements if 'Image' in str(type(el))]
# chunk_images[0].to_dict()




# for chunk in loaded_json:
#     if "Table" in str(type(chunk)):
#         tables.append(chunk)

#     if "CompositeElement" in str(type((chunk))):
#         texts.append(chunk)
# elements = loaded_json[3]["metadata"]["orig_elements"]
# chunk_images=[element for element in elements if "Image" in str(type(element))]
# print(chunk_images[0].to_dict())

# Get the images from the CompositeElement objects
# def get_images_base64(loaded_chunks):
#     images_b64 = []
#     for chunk in chunks:
#         if "CompositeElement" in str(type(chunk)):
#             chunk_els = chunk.metadata.orig_elements
#             for el in chunk_els:
#                 if "Image" in str(type(el)):
#                     images_b64.append(el.metadata.image_base64)
#     return images_b64

# images = get_images_base64(chunks)
# print(images[0])


# def display_base64_image(base64_code):
#     # Decode the base64 string to binary
#     try:
#        image_data = base64.b64decode(base64_code)
#     except DFInfoNotInstalledError as e:
#        print("Poppler is not installed or not in PATH. Please install it.")
#        raise e

#     display(Image(data=image_data))

# display_base64_image(images[0])


# def save_base64_image(base64_code, output_path):
#     image_data = base64.b64decode(base64_code)
#     with open(output_path, "wb") as f:
#         f.write(image_data)

# output_image_path = os.path.join(base_dir, "output_image.png")
# save_base64_image(images[0], output_image_path)

# print(f"Image saved at {output_image_path}")
# tables = []
# texts = []

# for chunk in loaded_json:
#     # Check for Table
#     if any("Table" in str(type(value)) for value in chunk.values()):
#         tables.append(chunk)
    
#     # Check for CompositeElement
#     if any("CompositeElement" in str(type(value)) for value in chunk.values()):
#         texts.append(chunk)
# for chunk in loaded_json:
#     for value in chunk.values():
#         if "CompositeElement" in str(type(value)):
#             # Check if this CompositeElement contains an image
#             if hasattr(value, 'image') and value.image is not None:
#                 # Assuming the image is stored as binary data (bytes), like PNG/JPEG content
#                 try:
#                     img = Image.open(io.BytesIO(value.image))
#                     plt.imshow(img)
#                     plt.axis('off')
#                     plt.show()
#                     break  # Stop after showing the first image
#                 except Exception as e:
#                     print(f"Error loading image: {e}")