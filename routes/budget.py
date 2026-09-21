from flask import Blueprint, render_template, request
from flask_login import login_required

budget_bp = Blueprint("budget", __name__, url_prefix="/budget")

def money(name):
    try: return float(request.form.get(name, 0) or 0)
    except ValueError: return 0

@budget_bp.route("/", methods=["GET", "POST"])
@login_required
def budget():
    values = {}
    result = None
    if request.method == "POST":
        fields = ["current_housing","new_housing","utilities","childcare","gas","vehicle","insurance","food","moving","reimbursement"]
        values = {f: money(f) for f in fields}
        current = values["current_housing"] + values["utilities"] + values["childcare"] + values["gas"] + values["vehicle"] + values["insurance"] + values["food"]
        new = values["new_housing"] + values["utilities"] + values["childcare"] + values["gas"] + values["vehicle"] + values["insurance"] + values["food"]
        result = {"current": current, "new": new, "difference": new-current, "estimated_pcs": max(values["moving"]-values["reimbursement"],0)}
    return render_template("budget.html", values=values, result=result)

