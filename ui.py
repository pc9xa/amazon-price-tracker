import streamlit as st
from scraper import Scraper
from PIL import Image
from io import BytesIO

# - Constants -------------------------------------------------------------------
DEBUG_MODE = False

# - Initialize ------------------------------------------------------------------
# - Session state
if "preview_image" not in st.session_state:
    st.session_state["preview_image"] = ""

if "tracking_counter" not in st.session_state:
    st.session_state["tracking_counter"] = 0

# - Scraper
sc = Scraper()

# - Database
sc.init_db()

# - Callbacks -------------------------------------------------------------------
def preview_product():
    if product_link.startswith("https://www.amazon.com/"):
        png_bytes = sc.get_product_screenshot(product_link)
        st.session_state["preview_image"] = Image.open(BytesIO(png_bytes))
    else:
        st.error('Something is wrong. Did you enter a link from Amazon? '
                 'Please make sure that the link starts with "https://www.amazon.com/"')

def save_product(save_product_link):
    with st.spinner(text="Adding product to list...", show_time=False):
        sc.save_product(save_product_link)
        st.session_state.product_link_k = ""

# - UI --------------------------------------------------------------------------
st.header("Amazon Price Tracker")
st.divider()

# - Enter product link
enter_product_c1, enter_product_c2 = st.columns([8.25, 1.25])
with enter_product_c1:
    product_link = st.text_input(
        label="Amazon product link",
        placeholder="https://www.amazon.com/...",
        key="product_link_k",
    )
with enter_product_c2:
    st.space("small")
    enter_button = st.button(
        label="Enter",
        key="enter_button_k",
        width="stretch",
        disabled=st.session_state["tracking_counter"] >= 5
    )

# - Limit monitored products to 5 at a time
st.session_state["tracking_counter"] = sc.get_product_list_size()
if st.session_state["tracking_counter"] >= 5:
    st.caption(
        "*You've hit the maximum number of products to monitor.\n"
        "Delete a product from the list below to monitor another product.*"
    )
else:
    st.caption(
        "*You can monitor the price of up to 5 products from Amazon.*"
    )

# - Product preview
if enter_button:
    with st.spinner(text="Checking product...", show_time=False):
        preview_product()
        with st.container(
                border=True,
                key="product_preview_k",
                height="stretch",
        ):
            st.text("Preview:")
            st.image(st.session_state["preview_image"])

        monitoring_button = st.button(
            label="Start monitoring this product",
            key="monitor_button_k",
            width="stretch",
            on_click=save_product,
            args=(product_link,),
        )

# - Product price monitoring interface
st.divider()
st.subheader(f"Tracked products ({st.session_state["tracking_counter"]}):")

#TODO: Add handling if no products saved
all_products = sc.load_all_tracked_products()
if isinstance(all_products, str):
    # Error message was returned instead of a list
    st.error(all_products)
elif not all_products:
    st.caption("You are not monitoring the price of any product at the moment. "
               "Use the field above to start monitoring prices!")
else:
    for i, product in enumerate(all_products):
        with st.container(
          border=True,
        ):
            df = sc.load_product_info(product)
            st.text(product)
            st.bar_chart(df, x="timestamp", y="price")
            tracked_product_c1, tracked_product_c2 = st.columns([7, 3])
            with tracked_product_c2:
                del_button = st.button(
                    label="Stop monitoring",
                    key=f"stop_button_k_{i}",
                    width="stretch",
                )
                if del_button:
                    with st.spinner(text="Removing this product from the monitor list...", show_time=False):
                        sc.del_one_product(product)
                        st.rerun()

#TODO: Timed fetching of price

# - Footer
st.space("large")
st.divider()
st.caption("by Patricia Ysabel Canencia, © 2026")

# - DEBUG CODE
if DEBUG_MODE:
    st.divider()
    "Session state: ", st.session_state