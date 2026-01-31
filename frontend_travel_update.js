// FRONTEND UPDATE REQUIRED: Separate Travel Categories

// OLD STRUCTURE (Single Travel Field):
{
  "spend": {
    "travel": 2000,  // ❌ Ambiguous - could be flights OR Careem
    "dining": 1500,
    "groceries": 1200
  }
}

// NEW STRUCTURE (Separated Travel Fields):
{
  "spend": {
    "international_travel": 2000,  // ✅ Flights, hotels, foreign spending
    "domestic_transport": 800,     // ✅ Careem, RTA, local transport
    "dining": 1500,
    "groceries": 1200
  }
}

// FRONTEND FORM CHANGES NEEDED:

// Replace single "Travel" input with two separate inputs:

1. "International Travel" 
   - Label: "International Travel (Flights, Hotels, Foreign Spending)"
   - Field: international_travel
   - Placeholder: "Monthly spending on flights, hotels abroad, foreign transactions"

2. "Local Transport"
   - Label: "Local Transport (Careem, RTA, Metro, Parking)"  
   - Field: domestic_transport
   - Placeholder: "Monthly spending on ride-hailing, metro, parking, tolls"

// CARD RECOMMENDATIONS IMPACT:

International Travel (2000+ AED/month):
✅ Amazon.ae Credit Card (2.5% international)
✅ Manchester City Titanium (10X international)
✅ Travel-focused airline cards

Domestic Transport (800+ AED/month):
✅ FAB Z Card (Free Careem Plus)
✅ Emirates NBD Go4it (Nol integration)
✅ Emirates NBD Flexi (Careem benefits)

// BACKWARD COMPATIBILITY:
// If old "travel" field exists, split it 70/30 or ask user to clarify