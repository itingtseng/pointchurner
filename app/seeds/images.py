import os
from app.models.db import db
from app.models.card import Card

def update_card_images():
    # Define the path to the seed-images directory
    seed_images_folder = os.path.join(os.path.dirname(__file__), 'seed-images')

    # Loop through all card IDs and update their image_url
    for card_id in range(1, 155):  # Card IDs are 1 to 154
        # Construct the image file name
        image_file = f"{card_id}.png"
        image_path = f"/seed-images/{image_file}"  # Relative path to the image

        # Check if the image exists in the directory
        if os.path.exists(os.path.join(seed_images_folder, image_file)):
            # Query the card by ID
            card = Card.query.get(card_id)
            if card:
                # Update the image_url field
                card.image_url = image_path
                db.session.add(card)
        else:
            print(f"Image file {image_file} not found for card ID {card_id}.")

    # Commit the changes to the database
    db.session.commit()
    print("Card images updated successfully.")

if __name__ == '__main__':
    update_card_images()
