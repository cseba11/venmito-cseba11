## **README: Venmito Data Engineering Project**  
**Author:** Carlos Hernandez Alvarado  
**Email:** [carlos.hernandez43@upr.edu](mailto:carlos.hernandez43@upr.edu)  
**University:** University of Puerto Rico at Mayaguez  

---

### **Project Description**

This project is part of the **Venmito Data Engineering Challenge**, where the goal was to process, filter, and analyze data from multiple file formats (`.json`, `.yml`, `.csv`, `.xml`). The data was cleaned, merged, and transformed into uniform Pandas DataFrames to derive meaningful insights and generate visualizations.

---

### **Solution Overview**

#### **1. Data Extraction and Transformation**  
- I started by reading files from the `data` folder in different formats (`.json`, `.yml`, `.csv`, `.xml`).  
- Each file was converted into a Pandas **DataFrame** for uniformity and easier analysis.  

#### **2. Merging People Data**  
- The `people.json` and `people.yml` files were merged into a single **People DataFrame**.  
- **Columns from `people.json`:** `id`, `first_name`, `last_name`, `telephone`, `email`.  
- **Columns from `people.yml`:** `Android`, `Desktop`, `iPhone`, `city`.  
- This ensured a unified structure for all people-related data.

#### **3. Filtering Promotions Data**  
- The `promotions.csv` file was filtered using the People DataFrame.  
- First, the data was merged using the **`telephone`** column with an **inner join**.  
- Next, another merge was performed using **`email` (left DataFrame)** and **`client_email` (right DataFrame)**.  
- A final merge with an **outer join** was executed to consolidate all information.

#### **4. Filtering Transfers Data**  
- The `transfers.csv` file was filtered by ensuring both `sender_id` and `recipient_id` exist in the People DataFrame.  
- This step ensures that only valid transfers between known people are retained.

#### **5. Filtering Transactions Data**  
- The `transactions.xml` file was filtered using the **`telephone`** column from the People DataFrame.  
- This ensured that only transactions related to people in the unified DataFrame were considered.

#### **6. Processed Data Files**  
- Filtered data was saved into the `data/processed` folder as `.csv` files:  
   - `people_filtered.csv`  
   - `promotions_filtered.csv`  
   - `transfers_filtered.csv`  
   - `transactions_filtered.csv`  

---

### **Data Analysis and Visualizations**

#### **1. Transactions Analysis (Best Sellers)**  
- Used a `groupby` operation on `item` and `quantity`.  
- Calculated the total quantity sold for each item.  
- **Visualization:** A **Line Plot** was generated with:  
   - **X-axis:** Item Names  
   - **Y-axis:** Total Quantity Sold  

#### **2. Transfers Analysis**  
- Analyzed `sender_id` and `recipient_id` to determine the total amount sent and received by each person.  
- Created an `amount_left` column (`amount_received - amount_sent`) to measure net balance.  

**Visualizations:**  
1. **Graph Plot:**  
   - **Nodes:** Represent person IDs.  
   - **Edges:** Represent the amount sent between individuals.  
2. **Tabular View:** Displaying columns:  
   - `id`, `amount_sent`, `amount_receive`, `amount_left`.  

#### **3. Promotions Analysis**  
- Grouped by `promotion` and counted how many clients responded "Yes".  
- Calculated the **percentage of positive responses** for each promotion.

**Visualizations:**  
1. **Combo Chart:**  
   - **X-axis:** Promotions  
   - **Y-axis:** Total Promotions  
   - Line plot showing the percentage of positive responses.  
2. **Pie Chart:**  
   - Displays the **Distribution of Yes Responses by Promotion**.  
   - The largest slice is highlighted to emphasize the promotion with the highest success rate.  

---

### **How to Run the Code**

1. **Clone the Repository:**  
   ```bash
   git clone <repository_url>
   cd <project_folder>

2. **Install Required Libraries:**  
   - **Pandas** 
   - **Matplotlib**  
   - **Networkx**  
   - **pyyaml**   
   pip install pandas matplotlib networkx pyyaml
