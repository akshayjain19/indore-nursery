from lib.util import wa_link


def plant_message(name):
    return wa_link(
        f"Hi Indore Nursery, I'm interested in {name}. Please share availability and details."
    )


def pot_message(name, size="", colour=""):
    parts = [f"Hi Indore Nursery, I'm interested in {name}"]
    if size:
        parts.append(f"size {size}")
    if colour:
        parts.append(colour)
    msg = ", ".join(parts) + ". Please share availability and details."
    return wa_link(msg)


def corporate_message():
    return wa_link(
        "Hi Indore Nursery, I'd like to enquire about corporate plant rental and greenery solutions."
    )


def landscaping_message():
    return wa_link(
        "Hi Indore Nursery, I'd like to discuss a landscaping requirement."
    )


def event_message():
    return wa_link(
        "Hi Indore Nursery, I'd like to enquire about plant decor for an event."
    )


def general_message():
    return wa_link(
        "Hi Indore Nursery, I'd like to know more about your plants, pots and green-space solutions."
    )
