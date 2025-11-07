from app.model.finance_model import FinanceInfo


def flatten_finance_info(finance_info: FinanceInfo) -> str:
    """
    Flatten the FinanceInfo object into a readable paragraph text.

    Args:
        finance_info: FinanceInfo object containing user's financial data

    Returns:
        Flattened finance information as text
    """
    parts = []

    # Export info summary
    if finance_info.export_info:
        export = finance_info.export_info
        parts.append(
            f"Financial data exported on {export.export_date} using app version {export.app_version}."
        )
        parts.append(
            f"Data format: {export.data_format}. "
            f"Total records: {export.total_transactions} transactions, "
            f"{export.total_accounts} accounts, {export.total_budgets} budgets."
        )

    # Account details
    if finance_info.accounts:
        parts.append(f"\n\nAccounts ({len(finance_info.accounts)} total):")
        for acc in finance_info.accounts:
            acc_info = f"- Account ID: {acc.id}"
            if acc.account_name:
                acc_info += f" | Name: {acc.account_name}"
            if acc.account_number:
                acc_info += f" | Number: {acc.account_number}"
            if acc.bank_name:
                acc_info += f" | Bank: {acc.bank_name}"
            if acc.account_type:
                acc_info += f" | Type: {acc.account_type}"
            if acc.balance is not None:
                acc_info += f" | Balance: ₹{acc.balance:.2f}"
            if acc.is_active is not None:
                acc_info += f" | Status: {'Active' if acc.is_active else 'Inactive'}"
            if acc.ifsc_code:
                acc_info += f" | IFSC: {acc.ifsc_code}"
            if acc.branch_name:
                acc_info += f" | Branch: {acc.branch_name}"
            if acc.description:
                acc_info += f" | Description: {acc.description}"
            if acc.created_at:
                acc_info += f" | Created: {acc.created_at}"
            if acc.updated_at:
                acc_info += f" | Updated: {acc.updated_at}"
            parts.append(acc_info)

    # Budget details
    if finance_info.budgets:
        parts.append(f"\n\nBudgets ({len(finance_info.budgets)} total):")
        for budget in finance_info.budgets:
            budget_info = f"- Budget ID: {budget.id} | Period: {budget.year}/{budget.month:02d} | Amount: ₹{budget.amount}"
            if budget.created_at:
                budget_info += f" | Created: {budget.created_at}"
            if budget.updated_at:
                budget_info += f" | Updated: {budget.updated_at}"
            parts.append(budget_info)

    # Transaction details
    if finance_info.transactions:
        parts.append(f"\n\nTransactions ({len(finance_info.transactions)} total):")

        # Summarize by transaction type
        credits = [
            t for t in finance_info.transactions if t.type and t.type.value == "credit"
        ]
        debits = [
            t for t in finance_info.transactions if t.type and t.type.value == "debit"
        ]
        transfers = [
            t
            for t in finance_info.transactions
            if t.type and t.type.value == "transfer"
        ]

        if credits:
            total_credits = sum(t.amount or 0 for t in credits)
            parts.append(
                f"  Credit transactions: {len(credits)} totaling ₹{total_credits:.2f}"
            )

        if debits:
            total_debits = sum(t.amount or 0 for t in debits)
            parts.append(
                f"  Debit transactions: {len(debits)} totaling ₹{total_debits:.2f}"
            )

        if transfers:
            total_transfers = sum(t.amount or 0 for t in transfers)
            parts.append(
                f"  Transfer transactions: {len(transfers)} totaling ₹{total_transfers:.2f}"
            )

        # Show all transactions with complete details
        parts.append("\n  All Transactions Details:")
        for trans in finance_info.transactions:
            trans_info = f"  - Transaction ID: {trans.id}"
            if trans.date:
                trans_info += f" | Date: {trans.date}"
            if trans.type:
                trans_info += f" | Type: {trans.type.value}"
            if trans.title:
                trans_info += f" | Title: {trans.title}"
            if trans.amount is not None:
                trans_info += f" | Amount: ₹{trans.amount:.2f}"
            if trans.category:
                trans_info += f" | Category: {trans.category.value}"
            if trans.account_id:
                trans_info += f" | Account ID: {trans.account_id}"
            if trans.location:
                trans_info += f" | Location: {trans.location}"
            if trans.description:
                trans_info += f" | Description: {trans.description}"
            if trans.sms_content:
                trans_info += f" | SMS: {trans.sms_content}"
            if trans.photos:
                trans_info += f" | Photos: {len(trans.photos)} attached"
            parts.append(trans_info)

    return "\n".join(parts)
