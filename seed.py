from app import create_app
from extensions import db
from models import (
    BAHRate,
    Base,
    ChildcareCenter,
    CredentialRule,
    InstallationResource,
    PCSChecklistItem,
    HousingCommunity,
    MedicalProvider,
    VehicleRule,
)

app = create_app()


def seed():
    with app.app_context():
        db.create_all()

        fort_bragg = Base.query.filter_by(name="Fort Bragg").first()
        camp_lejeune = Base.query.filter_by(name="Camp Lejeune").first()
        if not fort_bragg:
            fort_bragg = Base(name="Fort Bragg", state="NC", city="Fayetteville", branch="Army")
            db.session.add(fort_bragg)
        if not camp_lejeune:
            camp_lejeune = Base(name="Camp Lejeune", state="NC", city="Jacksonville", branch="Marine Corps")
            db.session.add(camp_lejeune)
        db.session.flush()

        if MedicalProvider.query.count() == 0:
            db.session.add_all([
                MedicalProvider(name="Womack Army Medical Center", base_id=fort_bragg.id, tricare_prime=True, tricare_select=True, pediatric=True, vaccine_policy="Verify current policy", category="Military Treatment Facility"),
                MedicalProvider(name="Pediatric Clinic Example", base_id=fort_bragg.id, tricare_prime=True, tricare_select=True, pediatric=True, vaccine_policy="Verify current policy", category="Pediatrics"),
                MedicalProvider(name="Naval Medical Center Camp Lejeune", base_id=camp_lejeune.id, tricare_prime=True, tricare_select=True, pediatric=True, vaccine_policy="Verify current policy", category="Military Treatment Facility"),
            ])

        if ChildcareCenter.query.count() == 0:
            db.session.add_all([
                ChildcareCenter(name="Fort Bragg CDC Example", base_id=fort_bragg.id, accepts_ccys=True, age_range="6 weeks–5 years", availability_status="Contact for availability"),
                ChildcareCenter(name="Camp Lejeune CDC Example", base_id=camp_lejeune.id, accepts_ccys=True, age_range="6 weeks–5 years", availability_status="Contact for availability"),
            ])

        if HousingCommunity.query.count() == 0:
            db.session.add_all([
                HousingCommunity(name="Fort Bragg Family Housing Example", base_id=fort_bragg.id, bedrooms="2–4 bedrooms", eligibility="Eligibility varies by rank/family size", housing_type="On-base", website="https://home.army.mil/bragg/"),
                HousingCommunity(name="Camp Lejeune Family Housing Example", base_id=camp_lejeune.id, bedrooms="2–4 bedrooms", eligibility="Eligibility varies by rank/family size", housing_type="On-base", website="https://www.lejeune.marines.mil/"),
            ])

        if BAHRate.query.count() == 0:
            # DEMO values for app development, not official current BAH rates.
            for base in [fort_bragg, camp_lejeune]:
                for grade, amount in [("E-4", 1500), ("E-5", 1700), ("E-6", 1900), ("E-7", 2100), ("O-1", 1800), ("O-2", 2000)]:
                    db.session.add(BAHRate(base_id=base.id, year=2026, pay_grade=grade, with_dependents=True, monthly_rate=amount, source_url="https://www.travel.dod.mil/Allowances/Basic-Allowance-for-Housing/"))
                    db.session.add(BAHRate(base_id=base.id, year=2026, pay_grade=grade, with_dependents=False, monthly_rate=max(amount - 250, 0), source_url="https://www.travel.dod.mil/Allowances/Basic-Allowance-for-Housing/"))

        if CredentialRule.query.count() == 0:
            db.session.add_all([
                CredentialRule(
                    profession="Cosmetology", origin_state="NC", destination_state="GA",
                    pathway="Military-spouse portability / Georgia board review",
                    documents="Current NC cosmetology license\nLicense verification/good standing\nMilitary PCS orders\nMarriage certificate if applying as a military spouse\nGovernment-issued ID\nGeorgia application and any board-required documents",
                    steps="Confirm Georgia board requirements\nAsk whether federal SCRA portability or Georgia military-spouse provisions apply to the specific credential\nSubmit the required application and supporting documents\nWait for written authorization before practicing if the board requires it",
                    notes="Example pathway only; Georgia's current board rules control. Do not treat this record as an automatic license transfer.",
                    source_url="https://sos.ga.gov/georgia-state-board-cosmetology-and-barbers", last_verified="2026-09-20"),
                CredentialRule(
                    profession="Real Estate / Realtor", origin_state="NC", destination_state="GA",
                    pathway="State reciprocity/endorsement + military-spouse portability review",
                    documents="Current NC real-estate license\nLicense history/good standing\nMilitary PCS orders\nMarriage certificate if applying as a military spouse\nGovernment-issued ID\nGeorgia real-estate application and required fees/documents",
                    steps="Review Georgia Real Estate Commission rules\nCheck reciprocity/recognition for the NC credential\nCheck SCRA military-spouse portability requirements\nSubmit the pathway required by the Georgia commission\nConfirm authorization before performing regulated activity",
                    notes="Example pathway only; real-estate licensing is state regulated and the destination commission determines eligibility.",
                    source_url="https://grec.state.ga.us/", last_verified="2026-09-20")
            ])

        if VehicleRule.query.count() == 0:
            db.session.add_all([
                VehicleRule(
                    state="NC", military_status="Active-duty service member",
                    benefit_type="Military registration option",
                    title="MVR-614 can support NC title/registration for eligible non-resident military owners",
                    description="North Carolina allows eligible active-duty service members stationed in NC to title a vehicle without a North Carolina driver license by using MVR-614 and the required out-of-state license and supporting information. The vehicle must be principally garaged in NC for at least six months each year.",
                    documents="Valid out-of-state driver license\nMilitary ID or proof of active-duty status\nNorth Carolina garaging address\nVehicle title/ownership documents\nRequired title and registration documents",
                    steps="Confirm you meet the non-resident military eligibility requirements\nComplete MVR-614 if applicable\nSubmit the required title/registration paperwork\nMaintain required NC liability insurance\nVerify the final fee and tax amount with NCDMV",
                    source_url="https://www.ncdot.gov/dmv/downloads/Documents/MVR-614.pdf", last_verified="2026-09-20"),
                VehicleRule(
                    state="NC", military_status="Active-duty service member",
                    benefit_type="Highway-use tax",
                    title="Military status does not create a blanket NC highway-use tax exemption",
                    description="NCDMV states that military personnel, including residents and non-residents registering a vehicle in North Carolina, are not exempt from the highway-use tax simply because of military status. Separate statutory exemptions may apply to specific transactions, so the transaction itself matters.",
                    documents="Vehicle title or ownership documents\nPurchase or transfer documentation, when applicable\nAny applicable exemption certification such as MVR-613",
                    steps="Identify whether the transaction is a purchase, title transfer, family transfer, or another transaction\nReview the applicable highway-use tax rule\nCheck whether a specific statutory exemption applies\nConfirm the amount or exemption with NCDMV before payment",
                    source_url="https://www.ncdot.gov/dmv/offices-services/military/Pages/default.aspx", last_verified="2026-09-20"),
                VehicleRule(
                    state="NC", military_status="Military spouse/dependent",
                    benefit_type="Military registration option",
                    title="Eligible military spouses/dependents can use MVR-614 in qualifying circumstances",
                    description="MVR-614 identifies active-duty service members and eligible dependents stationed in North Carolina as non-resident categories that may title a vehicle in NC without a NC driver license, subject to the form's requirements.",
                    documents="Valid out-of-state driver license\nProof of military dependent status\nNorth Carolina garaging address\nVehicle title/ownership documents",
                    steps="Confirm dependent eligibility\nComplete MVR-614 when applicable\nProvide the required out-of-state license and vehicle documents\nVerify registration, insurance, and tax requirements with NCDMV",
                    source_url="https://www.ncdot.gov/dmv/downloads/Documents/MVR-614.pdf", last_verified="2026-09-20"),
                VehicleRule(
                    state="NC", military_status="Veteran/retiree",
                    benefit_type="Military specialty plate",
                    title="Military and veteran specialty plates have separate eligibility rules",
                    description="North Carolina offers military-related specialty plates. MVR-33A is used by eligible military personnel and veterans to apply for a military-related specialty plate, with eligibility certified before the plate is issued.",
                    documents="MVR-33A\nProof required for the selected military/veteran plate\nCurrent registration/title information\nAny applicable plate fee",
                    steps="Select the military/veteran plate category\nComplete MVR-33A\nProvide required eligibility proof for certification\nSubmit the certified application to NCDMV",
                    source_url="https://www.ncdot.gov/dmv/downloads/Documents/MVR-33A.pdf", last_verified="2026-09-20"),
                VehicleRule(
                    state="NC", military_status="Other",
                    benefit_type="Tag & Tax Together",
                    title="NC combines annual registration renewal and vehicle property tax billing",
                    description="North Carolina's Tag & Tax Together system combines the annual vehicle registration renewal fee and vehicle property tax into one renewal notice/payment. The property-tax amount can vary based on the vehicle's assessed value and applicable factors.",
                    documents="Current registration information\nRenewal notice when received\nPayment method",
                    steps="Review the Tag & Tax Notice\nSeparate the registration fee from the property-tax amount for budgeting\nPay the combined amount by the due date\nUse the official NCDMV/NCDOR sources for the final bill",
                    source_url="https://www.ncdor.gov/taxes-forms/property-tax/tag-tax-together-project", last_verified="2026-09-20"),
            ])

        if PCSChecklistItem.query.count() == 0:
            tasks = [
                ("Review PCS orders and keep originals accessible", "Before PCS", "Documents", "Keep original orders and copies with you.", "ANY", False, False, False, False),
                ("Create/update your Plan My Move checklist", "Before PCS", "Planning", "Use an official PCS planning tool alongside MIL-App.", "ANY", False, False, False, False),
                ("Request school, medical and dental records", "Before PCS", "Family", "Request records early so they are available after arrival.", "ANY", True, False, False, False),
                ("Check housing and BAH information for the destination", "Before PCS", "Housing", "Review housing options and current official allowance information.", "ANY", False, False, False, False),
                ("Review vehicle registration and tax rules for the destination", "Before PCS", "Vehicle", "Check DMV and tax authority requirements before arrival.", "ANY", False, True, False, False),
                ("Check professional-license transfer requirements", "Before PCS", "Employment", "Contact the destination licensing board before practicing.", "ANY", False, False, True, False),
                ("Complete command-sponsorship and overseas requirements", "Before PCS", "OCONUS", "For overseas moves, verify command sponsorship and host-country requirements.", "OCONUS", False, False, False, False),
                ("Schedule household-goods and transportation actions", "During PCS", "Moving", "Coordinate shipments and transportation through official channels.", "ANY", False, False, False, False),
                ("Carry important documents during travel", "During PCS", "Documents", "Keep IDs, orders, vehicle and family documents accessible.", "ANY", False, False, False, False),
                ("Update DEERS and TRICARE after arrival", "After Arrival", "Healthcare", "Verify dependent records and healthcare enrollment after the move.", "ANY", True, False, False, False),
                ("Complete destination vehicle registration", "After Arrival", "Vehicle", "Follow the destination state's final registration process.", "ANY", False, True, False, False),
                ("Find childcare and school resources", "After Arrival", "Family", "Connect with local childcare and school liaison resources.", "ANY", True, False, False, False),
                ("Update address and local records", "After Arrival", "Administration", "Update agencies, insurance, utilities and other records as needed.", "ANY", False, False, False, False),
                ("Complete overseas newcomer and local orientation", "After Arrival", "OCONUS", "Use installation newcomer resources and sponsor support.", "OCONUS", False, False, False, False),
            ]
            for row in tasks:
                db.session.add(PCSChecklistItem(title=row[0], phase=row[1], category=row[2], description=row[3], move_type=row[4], requires_children=row[5], requires_vehicle=row[6], requires_license=row[7], requires_pets=row[8], source_url="https://planmymove.militaryonesource.mil/"))

        if InstallationResource.query.count() == 0:
            for base in [fort_bragg, camp_lejeune]:
                resources = [
                    ("Relocation", "Military & Family Support / Relocation Assistance", "Local relocation support, newcomer assistance and PCS planning.", "https://www.militaryonesource.mil/moving-pcs/plan-to-move/"),
                    ("PCS", "Plan My Move", "Official personalized PCS checklist and moving resources.", "https://planmymove.militaryonesource.mil/"),
                    ("Installation", "MilitaryINSTALLATIONS", "Installation-specific programs, services and contacts.", "https://installations.militaryonesource.mil/"),
                    ("Healthcare", "TRICARE", "Verify healthcare options and enrollment after a move.", "https://www.tricare.mil/"),
                    ("Childcare", "MilitaryChildCare", "Use the official childcare system to explore care options.", "https://www.militarychildcare.com/"),
                ]
                for cat,title,desc,url in resources:
                    db.session.add(InstallationResource(base_id=base.id, category=cat, title=title, description=desc, url=url, source_url=url, last_verified="2026-09-20"))

        db.session.commit()
        print("Seed complete. Demo BAH values are placeholders and must be replaced with verified current official data before production use.")


if __name__ == "__main__":
    seed()

