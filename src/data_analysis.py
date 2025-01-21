import os
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt


def transactions_filtered_analysis():
    df_transactions_filtered = pd.read_csv("data/processed/transactions_filtered.csv")

    best_sellers = df_transactions_filtered.groupby("item")["quantity"].sum()
    # Line chart for the best sellers
    plt.figure(figsize=(12, 6))
    plt.plot(best_sellers.index, best_sellers.values, marker="o", linestyle="-", color="orange")

    # Configure labels and title
    plt.xlabel("Item", fontsize=12)
    plt.ylabel("Total Quantity Sold", fontsize=12)
    plt.title("Best Sellers: Total Quantity Sold per Item", fontsize=14)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    # Display chart
    plt.show()   
    return best_sellers

def transfers_filtered_analysis():

    # Data Frame for the filtered data
    df_transfers_filtered = pd.read_csv("data/processed/transfers_filtered.csv")

    # Calculate the total sent (amount_sent) by each person
    amount_sent = df_transfers_filtered.groupby("sender_id")["amount"].sum().rename("amount_sent")

    # Calculate the total receive (amount_receive) by each person
    amount_receive = df_transfers_filtered.groupby("recipient_id")["amount"].sum().rename("amount_receive")

    df_amounts = pd.DataFrame({
        "id": pd.concat([amount_sent.index.to_series(), amount_receive.index.to_series()]).unique()
    })

    df_amounts = df_amounts.set_index("id")

    # Join the sent and received values
    df_amounts = df_amounts.join(amount_sent).join(amount_receive)
    
    # Llenar valores NaN con 0 (en caso de que alguien no haya enviado o recibido)
    df_amounts = df_amounts.fillna(0)

    # Calculate difference (amount_left) 
    df_amounts["amount_left"] = df_amounts["amount_receive"] - df_amounts["amount_sent"]

    # Reset the index to get a final DataFrame
    df_amounts = df_amounts.reset_index()
    
    
    # ---- CREATE GRAPH WITH NODES AND EDGES -> NODES ARE ID OF PEOPLE AND THE EDGES ARE THE AMOUNT SENT TO THE SPECIFIC ID ----
    
    G = nx.DiGraph()

    # Add nodes and edges to the graph with weights (amount sent)
    for _, row in df_transfers_filtered.iterrows():
        sender = row["sender_id"]
        recipient = row["recipient_id"]
        amount = row["amount"]
        G.add_edge(sender, recipient, weight=amount)  # Agregar arista con peso

    # Adjust the graph layout
    pos = nx.spring_layout(G, k=0.7, iterations=50)  # Aumentar k para mayor separación

    # Draw graph
    plt.figure(figsize=(12, 8))
    nx.draw(
        G, pos, with_labels=True, node_size=700, node_color="skyblue", font_size=10, edge_color="gray"
    )

    # Add labels for the edges (amount sent)
    edge_labels = {(u, v): f"${d['weight']}" for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

    # Title for the graph
    plt.title("Transfer Network: Sender → Recipient (Amount Sent)", fontsize=14)

    # Display final graph
    plt.tight_layout()
    plt.show()
    
    
    # ---- VISUAL TABLE WITH ID, AMOUNT_SENT, AMOUNT_RECEIVE AND AMOUNT LEFT ----
    
    # Adjust the figure size to occupy the entire screen
    fig, ax = plt.subplots(figsize=(16, 8))  # Cambia el tamaño para que sea más grande

    # Hide the graph and show only the table
    ax.axis('tight')
    ax.axis('off')
    table = ax.table(
        cellText=df_amounts.values,
        colLabels=df_amounts.columns,
        cellLoc='center',
        loc='center'
    )

    # Adjust the text size in the table
    table.auto_set_font_size(False)
    table.set_fontsize(14)  # Texto más grande para llenar la pantalla
    table.auto_set_column_width(col=list(range(len(df_amounts.columns))))  # Ajustar ancho de columnas

    # Summary Table Tittle
    plt.title("Summary Table: Sent, Received, and Net Amounts", fontsize=20)
    plt.show()

    return df_amounts

def promotions_filtered_analysis():

    df_promotions_filtered = pd.read_csv("data/processed/promotions_filtered.csv")

    promotion_stats = df_promotions_filtered.groupby("promotion").agg(
        total_promotions=("promotion", "count"),  # Total promotion by type
        responded_yes=("responded", lambda x: (x == "Yes").sum()),  # Total of "Yes" in responded
        percentage_yes=("responded", lambda x: round((x == "Yes").sum() / len(x) * 100, 2))  # Percentage of "Yes" by promotion
    ).reset_index()


    # ---- VISUAL BAR CHART WITH TOTAL PROMOTIONS AND PERCENTAGE YES ----

    fig, ax1 = plt.subplots(figsize=(10, 6))

    # Bar chart for the total promotions
    ax1.bar(
        promotion_stats["promotion"],
        promotion_stats["total_promotions"],
        color="skyblue",
        label="Total Promotions"
    )

    # Add a secondary Y axis for the percentage of "Yes"
    ax2 = ax1.twinx()  
    ax2.plot(
        promotion_stats["promotion"],
        promotion_stats["percentage_yes"],
        color="orange",
        marker="o",
        label="Percentage Yes"
    )

    # Tags and title
    ax1.set_xlabel("Promotions", fontsize=12)
    ax1.set_ylabel("Total Promotions", fontsize=12, color="blue")
    ax2.set_ylabel("Percentage Yes (%)", fontsize=12, color="orange")
    plt.title("Promotion Stats: Total and Percentage Yes", fontsize=14)

    # Change tags to vertical
    plt.xticks(rotation=45)

    ax1.legend(loc="upper left")
    ax2.legend(loc="upper right")

    # Display plot
    plt.tight_layout()
    plt.show()


    # ---- PASTEL CHART WITH DISTRIBUTION OF YES RESPONSES BY PROMOTION ----


    # Filter only promotions that have at least one "Yes"
    filtered_stats = promotion_stats[promotion_stats["responded_yes"] > 0]

    # Data for the chart
    labels = filtered_stats["promotion"]  
    sizes = filtered_stats["percentage_yes"] 
    explode = [0.1 if size == sizes.max() else 0 for size in sizes]  

    # Create the PASTEL chart
    plt.figure(figsize=(8, 8))
    plt.pie(
        sizes,
        labels=labels,
        autopct='%1.1f%%',  # Percentages to 1 decimal place
        startangle=140,  
        explode=explode,  # Highlight the largest slice with the larger "Yes" percentage
        colors=plt.cm.Paired.colors  # Friendly colors
    )

    # Tittle
    plt.title("Distribution of Yes Responses by Promotion", fontsize=14)

    # Display chart
    plt.show()



    return promotion_stats
    
    
