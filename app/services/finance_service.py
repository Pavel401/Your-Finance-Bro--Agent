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
            f"Total records: {export.total_transactions} transactions, "
            f"{export.total_accounts} accounts, {export.total_budgets} budgets."
        )

    # Account details
    if finance_info.accounts:
        parts.append(f"\n\nAccounts ({len(finance_info.accounts)} total):")
        for acc in finance_info.accounts:
            acc_info = f"- {acc.account_name or 'Unnamed Account'}"
            if acc.bank_name:
                acc_info += f" at {acc.bank_name}"
            if acc.account_type:
                acc_info += f" ({acc.account_type})"
            if acc.balance is not None:
                acc_info += f": Balance ${acc.balance:.2f}"
            if acc.is_active is not None:
                acc_info += f" - {'Active' if acc.is_active else 'Inactive'}"
            parts.append(acc_info)

    # Budget details
    if finance_info.budgets:
        parts.append(f"\n\nBudgets ({len(finance_info.budgets)} total):")
        for budget in finance_info.budgets:
            parts.append(f"- {budget.year}/{budget.month:02d}: ${budget.amount}")

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
                f"  Credit transactions: {len(credits)} totaling ${total_credits:.2f}"
            )

        if debits:
            total_debits = sum(t.amount or 0 for t in debits)
            parts.append(
                f"  Debit transactions: {len(debits)} totaling ${total_debits:.2f}"
            )

        if transfers:
            parts.append(f"  Transfer transactions: {len(transfers)}")

        # Show recent transactions (limit to 10 for context)
        parts.append("\n  Recent transactions:")
        for trans in finance_info.transactions[:10]:
            trans_info = f"  - {trans.date}: {trans.title or 'Untitled'}"
            if trans.type:
                trans_info += f" [{trans.type.value}]"
            if trans.amount is not None:
                trans_info += f" ${trans.amount:.2f}"
            if trans.category:
                trans_info += f" - {trans.category.value}"
            if trans.description:
                trans_info += f" - {trans.description}"
            parts.append(trans_info)

    return "\n".join(parts)
