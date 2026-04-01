<h1>Amazon price tracker (In progress)</h1>
A simple web-scraping tool that monitors prices of up to 5 Amazon products and sends an e-mail notification when the price drops below a user-defined threshold.

<h2>Project Status</h2>
🚧 This project is currently <strong>in progress</strong> and actively being improved on.
Features and structure may change over time.

<h2>Components & Architecture</h2>
<ul>
  <li><strong>Frontend: Streamlit UI</strong></li>
  <ul>
    <li>Input field for Amazon product links</li>
    <li>Displays price trends via graphs</li>
    <li>Supports tracking of up to 5 products simultaneously</li>
  </ul>
  <li><strong>Backend: Python + Selenium</strong></li>
  <ul>
    <li>Automates browser interaction</li>
    <li>Scrapes product price data from the Amazon product page</li>
  </ul>
  <li><strong>Database: SQLite</strong></li>
  <ul>
    <li>Stores monitored product and price information for visualization</li>
  </ul>
</ul>

<h2>Workflow</h2>
<ol>
  <li>User inputs an Amazon product URL via the Streamlit UI</li>
  <li>Selenium scraper takes a product screenshot and displays it in Streamlit as a prompt for confirmation</li>
  <li>User confirms the start of price monitoring for that product, and a graph for that product is displayed in the Streamlit UI</li>
  <li>If the graph drops below the defined threshold, an e-mail notification is sent.</li>
</ol>


<h2>Planned/ Upcoming Feautures</h2>
<ul>
  <li>Automated/ scheduled price checks</li>
  <li>E-mail notification feature</li>
  <li>Deploy Streamlit app (non-local)
  <li>Migrate local DB to Supabase or others (under consideration)</li>
</ul>
