import streamlit as st
from collections import deque

# =========================================================
# SPLITEASE - EXPENSE SETTLEMENT SYSTEM
# DATA STRUCTURES:
# 1. Queue - Settlement processing (FIFO)
# 2. List - Store members and expenses
# 3. Dictionary - Store member balances
# =========================================================

st.set_page_config(
    page_title="SplitEase",
    page_icon="💸",
    layout="wide"
)

# =========================================================
# SESSION STATE
# =========================================================

if "members" not in st.session_state:
    st.session_state.members = []

if "expenses" not in st.session_state:
    st.session_state.expenses = []

if "settlement_queue" not in st.session_state:
    st.session_state.settlement_queue = deque()

# =========================================================
# HEADER
# =========================================================

st.title("💸 SplitEase")

st.subheader("Queue-Based Expense Settlement System")

st.write(
    "A simple expense splitting system that uses a Queue "
    "to manage settlements using the FIFO principle."
)

# =========================================================
# DATA STRUCTURE DISPLAY
# =========================================================

st.markdown("### 🧠 Data Structures Used")

col1, col2, col3 = st.columns(3)

with col1:
    st.info("🔵 **Queue**\n\nFIFO – First In, First Out")

with col2:
    st.info("🟢 **List**\n\nStores members and expenses")

with col3:
    st.info("🟠 **Dictionary**\n\nStores member balances")

st.divider()

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("⚙️ SplitEase Menu")

menu = st.sidebar.radio(
    "Select Operation",
    [
        "👥 Add Members",
        "💰 Add Expense",
        "📊 Calculate Split",
        "📋 Expense History",
        "🚶 Settlement Queue",
        "ℹ️ About"
    ]
)

# =========================================================
# ADD MEMBERS
# =========================================================

if menu == "👥 Add Members":

    st.header("👥 Add Group Members")

    name = st.text_input(
        "Enter Member Name",
        placeholder="Example: Thamilselvan"
    )

    if st.button("➕ Add Member", use_container_width=True):

        name = name.strip()

        if name == "":
            st.error("Please enter a member name.")

        elif name in st.session_state.members:
            st.warning("This member already exists.")

        else:
            st.session_state.members.append(name)
            st.success(f"✅ {name} added successfully!")

    st.divider()

    st.subheader("Current Members")

    if len(st.session_state.members) == 0:
        st.info("No members added yet.")

    else:
        for i, member in enumerate(st.session_state.members, start=1):
            st.write(f"**{i}.** {member}")

# =========================================================
# ADD EXPENSE
# =========================================================

elif menu == "💰 Add Expense":

    st.header("💰 Add Expense")

    if len(st.session_state.members) == 0:

        st.warning("Please add members first.")

    else:

        description = st.text_input(
            "Expense Description",
            placeholder="Example: Dinner"
        )

        amount = st.number_input(
            "Expense Amount (₹)",
            min_value=0.0,
            step=10.0
        )

        paid_by = st.selectbox(
            "Paid By",
            st.session_state.members
        )

        if st.button("💾 Add Expense", use_container_width=True):

            if description.strip() == "":
                st.error("Please enter an expense description.")

            elif amount <= 0:
                st.error("Amount must be greater than ₹0.")

            else:

                expense = {
                    "description": description.strip(),
                    "amount": amount,
                    "paid_by": paid_by
                }

                st.session_state.expenses.append(expense)

                st.success(
                    f"✅ ₹{amount:.2f} expense added by {paid_by}!"
                )

# =========================================================
# CALCULATE SPLIT
# =========================================================

elif menu == "📊 Calculate Split":

    st.header("📊 Expense Split")

    if len(st.session_state.members) == 0:

        st.warning("Please add members first.")

    elif len(st.session_state.expenses) == 0:

        st.warning("Please add at least one expense.")

    else:

        # Dictionary for balances
        paid_amount = {
            member: 0.0
            for member in st.session_state.members
        }

        total_expense = 0.0

        # Calculate total and individual payments
        for expense in st.session_state.expenses:

            total_expense += expense["amount"]

            paid_amount[expense["paid_by"]] += expense["amount"]

        member_count = len(st.session_state.members)

        equal_share = total_expense / member_count

        # Calculate balances
        balances = {}

        for member in st.session_state.members:

            balances[member] = (
                paid_amount[member] - equal_share
            )

        # Display summary
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "💰 Total Expense",
                f"₹{total_expense:.2f}"
            )

        with col2:
            st.metric(
                "👥 Members",
                member_count
            )

        with col3:
            st.metric(
                "📌 Each Person",
                f"₹{equal_share:.2f}"
            )

        st.divider()

        st.subheader("📋 Member Summary")

        for member in st.session_state.members:

            paid = paid_amount[member]
            balance = balances[member]

            col1, col2, col3 = st.columns(3)

            with col1:
                st.write(f"**{member}**")

            with col2:
                st.write(f"Paid: ₹{paid:.2f}")

            with col3:

                if balance > 0:
                    st.success(
                        f"Gets ₹{balance:.2f}"
                    )

                elif balance < 0:
                    st.error(
                        f"Owes ₹{abs(balance):.2f}"
                    )

                else:
                    st.info("Settled")

        st.divider()

        # =================================================
        # CREATE SETTLEMENT QUEUE
        # =================================================

        if st.button(
            "🔄 Generate Settlement Queue",
            use_container_width=True
        ):

            # Clear old queue
            st.session_state.settlement_queue = deque()

            creditors = []
            debtors = []

            for member, balance in balances.items():

                if balance > 0.01:

                    creditors.append(
                        [member, balance]
                    )

                elif balance < -0.01:

                    debtors.append(
                        [member, abs(balance)]
                    )

            i = 0
            j = 0

            # Create settlements
            while i < len(debtors) and j < len(creditors):

                debtor = debtors[i]
                creditor = creditors[j]

                payment = min(
                    debtor[1],
                    creditor[1]
                )

                settlement = {
                    "from": debtor[0],
                    "to": creditor[0],
                    "amount": payment
                }

                # Add to Queue
                st.session_state.settlement_queue.append(
                    settlement
                )

                debtor[1] -= payment
                creditor[1] -= payment

                if debtor[1] <= 0.01:
                    i += 1

                if creditor[1] <= 0.01:
                    j += 1

            st.success(
                "✅ Settlement Queue generated successfully!"
            )

# =========================================================
# EXPENSE HISTORY
# =========================================================

elif menu == "📋 Expense History":

    st.header("📋 Expense History")

    if len(st.session_state.expenses) == 0:

        st.info("No expenses added yet.")

    else:

        for i, expense in enumerate(
            st.session_state.expenses,
            start=1
        ):

            st.write(
                f"**{i}. {expense['description']}**  "
                f"— ₹{expense['amount']:.2f}  "
                f"— Paid by **{expense['paid_by']}**"
            )

# =========================================================
# SETTLEMENT QUEUE
# =========================================================

elif menu == "🚶 Settlement Queue":

    st.header("🚶 Settlement Queue")

    st.write(
        "Queue follows **FIFO – First In, First Out**."
    )

    st.divider()

    queue = st.session_state.settlement_queue

    # Queue status
    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "📦 Pending Settlements",
            len(queue)
        )

    with col2:

        if len(queue) == 0:
            st.metric("🚦 Status", "Empty")
        else:
            st.metric("🚦 Status", "Active")

    st.divider()

    if len(queue) == 0:

        st.info(
            "Settlement Queue is empty. "
            "Go to Calculate Split and generate the queue."
        )

    else:

        st.subheader("📋 Current Queue")

        # Display queue
        for i, settlement in enumerate(
            queue,
            start=1
        ):

            if i == 1:
                st.success(
                    f"🔵 FRONT → {settlement['from']} "
                    f"pays ₹{settlement['amount']:.2f} "
                    f"to {settlement['to']}"
                )

            else:
                st.write(
                    f"➡️ {settlement['from']} "
                    f"pays ₹{settlement['amount']:.2f} "
                    f"to {settlement['to']}"
                )

        st.write("🔴 REAR")

        st.divider()

        # Process first settlement
        if st.button(
            "▶️ Process First Settlement",
            use_container_width=True
        ):

            processed = queue.popleft()

            st.success(
                f"✅ Processed: "
                f"{processed['from']} pays "
                f"₹{processed['amount']:.2f} "
                f"to {processed['to']}"
            )

            st.rerun()

        # Clear queue
        if st.button(
            "🗑️ Clear Queue",
            use_container_width=True
        ):

            st.session_state.settlement_queue.clear()

            st.success("✅ Queue cleared!")

            st.rerun()

# =========================================================
# ABOUT
# =========================================================

elif menu == "ℹ️ About":

    st.header("ℹ️ About SplitEase")

    st.write(
        "SplitEase is an expense settlement system designed "
        "using Data Structures in Python."
    )

    st.subheader("🎯 Main Data Structure")

    st.write(
        "**Queue – FIFO (First In, First Out)**"
    )

    st.write(
        "The Queue stores pending settlements. "
        "The first settlement added is processed first."
    )

    st.subheader("🧠 Other Data Structures")

    st.write("• **List** – Stores members and expenses.")
    st.write("• **Dictionary** – Stores member payment balances.")
    st.write("• **Queue** – Manages settlement processing.")

    st.subheader("⚙️ Technologies")

    st.write("• Streamlit")
    st.write("• Queue (collections.deque)")

    st.success(
        "SplitEase demonstrates the practical use "
        "of Queue in a real-world application."
    )