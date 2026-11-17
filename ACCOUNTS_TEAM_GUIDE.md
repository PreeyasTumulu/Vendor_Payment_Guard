# Vendor Payment Guard: a guide for the accounts team

This guide is for the people who process and pay supplier invoices. You don't need any technical knowledge to follow it.

## What the tool is for

Vendor Payment Guard looks at a supplier invoice before you pay it and tells you whether it's safe to go ahead.

It exists because of one particular kind of fraud. Someone gets into a supplier's email account, or creates one that
looks almost the same, and sends you an invoice that seems completely normal. The supplier name, the order number and
the amount are all correct. The only thing that has changed is the bank account, which now belongs to the fraudster.
Often the email says something like "please note our new bank details". If the payment goes through, the money is
usually gone for good. Companies in India have lost crores of rupees this way.

The tool doesn't replace you. It does the routine checking quickly and the same way every time, and it points out
the invoices that need a closer look.

## What it needs from the invoice

For each invoice, the tool needs six details:

| Detail | Example |
|---|---|
| Invoice number | SST/2026/0412 |
| Supplier name | Sharma Steel Traders |
| Purchase order (PO) number | PO-1001 |
| Amount | 450000 |
| Supplier's GSTIN | 27AABCS1234F1Z5 |
| Bank account to pay into | 50100234567 |

The tool reads these from the invoice text. It reads our standard invoice layout most reliably, where each detail is on
its own line, like `PO Number: PO-1001`. It can also read an invoice written as a normal email ("please find our bill
no. ... against your order PO-1001 ..."), but if it can't find a detail with certainty it treats that detail as missing
rather than guessing.

## What it checks

Once it has the six details, the tool compares the invoice with our own records and asks four questions:

1. Have we already paid this invoice? Suppliers sometimes resend old invoices by mistake, and fraudsters sometimes resend them on purpose.
2. Does it match a purchase order we actually raised, for that supplier? Is the amount within what we agreed? Have the goods been received?
3. Is the bank account the same one we have on record for this supplier?
4. Is the GST number valid, and does it belong to this supplier?

## How it decides

Every problem it finds adds points to a risk score. Some problems are more serious than others:

| Problem | Points |
|---|---|
| Invoice already paid | 100 |
| Bank account is different from our records | 50 |
| No matching purchase order | 40 |
| GST number is not valid | 40 |
| GST number belongs to a different company | 40 |
| Amount is more than the purchase order | 30 |
| Goods not received yet | 30 |

If nothing is wrong, the score is 0. Then:

- a score under 30 means the invoice is approved;
- a score of 80 or more means it is blocked;
- anything in between means the supplier needs to be phoned to confirm the invoice before anything is paid.

For example, an invoice where only the bank account has changed scores 50, so it leads to a phone call. An invoice with
a changed bank account and a fake GST number scores 90 and is blocked straight away.

## The phone call

When an invoice needs confirming, the supplier is called on the phone number in our own records. This matters: the
number printed on the invoice or in the email could belong to the fraudster, who will of course say everything is fine.

The question is simple: did you send this invoice, with these bank details?

- If the supplier confirms, the invoice is approved.
- If the supplier says they didn't send it, the invoice is blocked. This is very likely an attempted fraud.
- If nobody answers, the call is tried again, up to three times in total. If there's still no answer, the invoice is blocked until someone can confirm it.

In this version of the tool the phone calls are simulated, so that it can be tested and demonstrated. In real use, a
member of the team would make the call, always on the number from our records.

## What each result means and what to do

The tool always gives one of three results, together with a short reason.

### Approved

The invoice matches our records, or the supplier confirmed it by phone. You can pay it in the usual way.

### Blocked

Don't pay this invoice. What to do next depends on the reason:

| Reason shown | What it means | What to do |
|---|---|---|
| risk score 100 is too high (already paid) | we've paid this invoice before | Don't pay it again. Check the payment history and let the supplier know it was already paid. |
| vendor says they never sent this invoice, likely fraud | someone else sent it | Don't reply to the email or call any number in it. Tell your manager or the finance head straight away and keep the email as evidence. Let the supplier know their email may have been compromised. |
| could not reach vendor after 3 calls, unverified | we couldn't confirm it | Hold the payment. Try the supplier again later, on the number in our records. Only release the payment once they confirm. |
| risk score is too high (several problems) | more than one serious problem was found | Treat it as suspicious. Pass it to your manager to review before anything is paid. |

### Rejected

The invoice couldn't be checked at all, so it hasn't been approved or blocked. The reason tells you why:

- Missing details (for example "missing po_number; missing amount"): ask the supplier for a complete invoice, or check whether the details are on another page.
- Supplier not in our records: this might be a new supplier who hasn't been set up yet, or a fake name. Follow the normal process for adding a new supplier before paying anything.

## Reading a result

A result looks something like this:

```
Decision: BLOCKED
Reason:   vendor says they never sent this invoice - likely FRAUD
Problems found: BANK_DETAILS_CHANGED
Risk score: 50
Calls made: 1
```

The tool also keeps a step-by-step history of what it did with each invoice: what it read, what each check found, the
score, each phone call and the final decision. If anyone later asks why an invoice was paid or stopped, that history
has the answer.

## Good habits that go with the tool

The tool catches a lot, but these habits matter just as much:

- Never change a supplier's bank details because of an email, however genuine it looks. Confirm by phone, on the number we already have, and follow the proper process for updating records.
- Never use contact details from the invoice or email when checking whether it's real.
- Be extra careful with urgent requests ("please pay today, the director has approved it"). Pressure to hurry is a common sign of fraud.
- If something feels wrong even though the tool approved it, stop and ask. The tool only checks the things it has been told to check.

## Common questions

**A genuine invoice was blocked. Can I just pay it anyway?**
Not on your own. Bring it to your manager or the finance head. Most of the time the fix is simple, such as confirming
with the supplier by phone or updating our records, and then the invoice can be checked again.

**The supplier really has changed their bank. What now?**
Confirm it with them by phone on the number we have on file. Then update the supplier's details through the normal
approval process. Once our records show the new account, their invoices will pass the bank check again.

**Why did it reject an invoice that looks fine to me?**
Usually because a detail is missing or written in a way the tool couldn't read with certainty, often the PO number or the
amount. Check the invoice for those six details. If they're all there, ask whoever runs the tool to look at it.

**Does the tool make the payment?**
No. It only tells you whether the invoice is safe to pay. Paying is still done by the team in the usual way.

## Things to know about this version

This is a working prototype built for a college project. It uses a small set of sample suppliers, purchase orders and
past payments rather than our real accounting system, and the phone calls are simulated. Before using it for real
payments, it would need to be connected to the company's records, with a real person making the confirmation calls.

## Words used in this guide

| Word | Meaning |
|---|---|
| PO (purchase order) | the order we raised with the supplier, including the agreed amount |
| GRN (goods receipt note) | our record that the goods have arrived |
| GSTIN | the supplier's 15-character GST registration number |
| risk score | the total of the points for all problems found on an invoice |
| records | our own saved details for each supplier: name, GSTIN, bank account and phone number |
