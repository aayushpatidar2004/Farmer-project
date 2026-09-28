"""
Management command: load_sample_data

Loads clearly labelled demo/sample data for:
  - Crop Diseases and Pesticides
  - Agricultural Market Prices

Usage:
    python manage.py load_sample_data
    python manage.py load_sample_data --clear   # Removes existing sample data first

This data is for DEMONSTRATION PURPOSES ONLY and does not represent
live market prices or certified agricultural advice.
"""
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from datetime import date

from crops.models import Crop
from diseases.models import Disease, Pesticide
from market.models import MarketPrice
from soil.models import SoilData


DISEASE_DATA = [
    {
        "crop_name": "Rice",
        "disease_name": "Rice Blast",
        "severity": "high",
        "symptoms": (
            "Diamond-shaped lesions with grey-white centres on leaves, panicle neck rot, "
            "grain discolouration. Lesions can coalesce and kill entire leaves."
        ),
        "causes": (
            "Caused by the fungus Magnaporthe oryzae (Pyricularia oryzae). "
            "Spreads through infected seeds, wind-borne spores, and crop residue. "
            "Favoured by temperatures 25–28 °C with high humidity and night dew."
        ),
        "prevention": (
            "Use certified blast-resistant varieties (e.g., Pusa Basmati 1460). "
            "Avoid excess nitrogen application. Maintain field hygiene and remove crop residue. "
            "Use healthy, certified seed. Avoid dense planting."
        ),
        "treatment": (
            "Apply Tricyclazole (75% WP) at 0.6 g/litre at the appearance of first lesions. "
            "Repeat spray after 10 days if required. Alternatively use Isoprothiolane or Carbendazim."
        ),
        "pesticides": [
            {
                "name": "Tricyclazole 75% WP",
                "pesticide_type": "fungicide",
                "active_ingredient": "Tricyclazole",
                "dosage": "0.6 g per litre of water; 200–250 litres/ha",
                "application_method": "Foliar spray; spray to wet both leaf surfaces. Repeat after 10–12 days if needed.",
                "safety_notes": "Wear protective gloves and mask. Do not spray near water bodies. PHI: 14 days.",
            },
        ],
    },
    {
        "crop_name": "Wheat",
        "disease_name": "Yellow Rust (Stripe Rust)",
        "severity": "high",
        "symptoms": (
            "Yellow-orange stripes of pustules running parallel to leaf veins. "
            "Severely infected leaves turn yellow and dry out. Occurs mainly in cool, moist weather."
        ),
        "causes": (
            "Caused by Puccinia striiformis f. sp. tritici. "
            "Favoured by temperatures 10–15 °C with high humidity. Spreads via airborne urediniospores."
        ),
        "prevention": (
            "Grow resistant varieties (e.g., HD 2781, K 307). "
            "Avoid late sowing. Monitor crops regularly from January."
        ),
        "treatment": (
            "Apply Propiconazole 25% EC at 0.1% solution (1 ml/litre) at first sign of disease. "
            "A second spray 15 days later may be needed in severe infections."
        ),
        "pesticides": [
            {
                "name": "Propiconazole 25% EC",
                "pesticide_type": "fungicide",
                "active_ingredient": "Propiconazole",
                "dosage": "1 ml per litre of water; 200 litres/ha",
                "application_method": "Foliar spray at full canopy coverage. Repeat after 15 days if needed.",
                "safety_notes": "Avoid contact with eyes and skin. Do not spray during windy conditions. PHI: 21 days.",
            },
        ],
    },
    {
        "crop_name": "Tomato",
        "disease_name": "Early Blight",
        "severity": "medium",
        "symptoms": (
            "Dark brown to black lesions with concentric rings (target board pattern) on older leaves. "
            "Lesions may have yellow halos. Severe infection causes complete defoliation."
        ),
        "causes": (
            "Caused by Alternaria solani. "
            "Favoured by warm temperatures (24–29 °C) with alternating wet and dry periods. "
            "Spreads through infected plant debris and soil."
        ),
        "prevention": (
            "Use disease-free transplants. Remove and destroy infected plant parts promptly. "
            "Practice crop rotation (avoid nightshades for 2–3 years). "
            "Stake plants to improve air circulation."
        ),
        "treatment": (
            "Apply Mancozeb 75% WP at 2.5 g/litre or Copper oxychloride 50% WP at 3 g/litre. "
            "Begin sprays preventively before disease onset; repeat every 7–10 days."
        ),
        "pesticides": [
            {
                "name": "Mancozeb 75% WP",
                "pesticide_type": "fungicide",
                "active_ingredient": "Mancozeb",
                "dosage": "2.5 g per litre of water; 200–400 litres/ha",
                "application_method": "Foliar spray; start before disease onset. Repeat every 7–10 days.",
                "safety_notes": "Avoid inhalation of dust. Keep away from children. PHI: 7 days for tomato.",
            },
        ],
    },
    {
        "crop_name": "Cotton",
        "disease_name": "Cotton Bollworm",
        "severity": "critical",
        "symptoms": (
            "Holes in buds, flowers, and bolls. Frass (excrement) visible at entry holes. "
            "Damaged bolls open prematurely. Young larvae feed on leaf tissue and squares."
        ),
        "causes": (
            "Helicoverpa armigera (American bollworm). "
            "Polyphagous pest, highly destructive. Favoured by dry weather and high temperatures."
        ),
        "prevention": (
            "Use Bt-transgenic cotton varieties where approved. "
            "Set up pheromone traps (5/ha) for monitoring. "
            "Encourage natural predators. Avoid excess nitrogen which promotes vegetative growth."
        ),
        "treatment": (
            "Apply Emamectin benzoate 5% SG at 0.4 g/litre when early instar larvae are observed. "
            "Rotate with Indoxacarb 14.5% SC to prevent resistance build-up."
        ),
        "pesticides": [
            {
                "name": "Emamectin Benzoate 5% SG",
                "pesticide_type": "insecticide",
                "active_ingredient": "Emamectin Benzoate",
                "dosage": "0.4 g per litre of water; 200–250 litres/ha",
                "application_method": "Foliar spray targeting larval stage. Cover plant well. PHI: 3 days.",
                "safety_notes": "Highly toxic to bees; avoid spraying during flowering. Wear PPE.",
            },
        ],
    },
    {
        "crop_name": "Potato",
        "disease_name": "Late Blight",
        "severity": "critical",
        "symptoms": (
            "Water-soaked, dark lesions on leaves, especially at leaf margins. "
            "White downy fungal growth on the underside in humid conditions. "
            "Tubers show dark, rotten areas internally."
        ),
        "causes": (
            "Caused by Phytophthora infestans. "
            "Most destructive in cool (10–20 °C), wet weather. "
            "Spreads rapidly via windborne sporangia."
        ),
        "prevention": (
            "Plant certified disease-free seed tubers. "
            "Use resistant varieties. "
            "Avoid overhead irrigation. Improve field drainage. Hilling reduces tuber infection."
        ),
        "treatment": (
            "Apply Metalaxyl + Mancozeb (Ridomil Gold) at 2.5 g/litre preventively, starting 3 weeks after emergence. "
            "Use Cymoxanil + Mancozeb during active disease. Repeat every 7 days in wet weather."
        ),
        "pesticides": [
            {
                "name": "Metalaxyl 8% + Mancozeb 64% WP",
                "pesticide_type": "fungicide",
                "active_ingredient": "Metalaxyl + Mancozeb",
                "dosage": "2.5 g per litre of water; 200–400 litres/ha",
                "application_method": "Foliar spray. Start preventively; repeat every 7 days in rainy weather.",
                "safety_notes": "Avoid contact with skin and eyes. PHI: 14 days.",
            },
        ],
    },
    {
        "crop_name": "Maize",
        "disease_name": "Maize Stalk Rot",
        "severity": "high",
        "symptoms": (
            "Premature death of lower leaves (firing). Stalk becomes soft and discoloured internally. "
            "Lodging of plants. Stalk emits foul odour when cut."
        ),
        "causes": (
            "Complex caused by Fusarium spp. and Pythium spp. "
            "Favoured by water stress followed by irrigation and high temperatures during grain fill. "
            "Plants weakened by poor nutrition are more susceptible."
        ),
        "prevention": (
            "Use tolerant hybrids. "
            "Avoid stress during grain fill through adequate irrigation and balanced nutrition. "
            "Crop rotation with non-host crops. Early harvest reduces losses."
        ),
        "treatment": (
            "No effective curative treatment once stalk rot is established. "
            "Preventive seed treatment with Carbendazim (2 g/kg seed) reduces early infections. "
            "Harvest early when 50% of plants show lower leaf death."
        ),
        "pesticides": [
            {
                "name": "Carbendazim 50% WP (Seed Treatment)",
                "pesticide_type": "fungicide",
                "active_ingredient": "Carbendazim",
                "dosage": "2 g per kg of seed",
                "application_method": "Dry seed treatment before sowing. Mix uniformly with seed.",
                "safety_notes": "Avoid inhalation during mixing. Use gloves. Treated seed is not for human consumption.",
            },
        ],
    },
    {
        "crop_name": "Groundnut",
        "disease_name": "Tikka Disease (Leaf Spot)",
        "severity": "medium",
        "symptoms": (
            "Small circular spots — early leaf spot has dark brown colour; late leaf spot has dark almost black colour. "
            "Severe infection causes defoliation, reducing yield and pod quality."
        ),
        "causes": (
            "Early leaf spot: Cercospora arachidicola. "
            "Late leaf spot: Phaeoisariopsis personata. "
            "Both spread via conidia in warm (25–30 °C) wet conditions."
        ),
        "prevention": (
            "Use resistant varieties. "
            "Crop rotation (avoid groundnut for 2 years). "
            "Remove and destroy infected plant debris. Avoid dense planting."
        ),
        "treatment": (
            "Apply Chlorothalonil 75% WP at 2 g/litre or Tebuconazole 25.9% EC at 1 ml/litre. "
            "Begin sprays at first appearance; repeat every 10–14 days."
        ),
        "pesticides": [
            {
                "name": "Chlorothalonil 75% WP",
                "pesticide_type": "fungicide",
                "active_ingredient": "Chlorothalonil",
                "dosage": "2 g per litre of water; 200 litres/ha",
                "application_method": "Foliar spray at first sign of disease. Repeat every 10–14 days.",
                "safety_notes": "Use protective equipment. Do not spray near water bodies. PHI: 7 days.",
            },
        ],
    },
    {
        "crop_name": "Sugarcane",
        "disease_name": "Red Rot",
        "severity": "high",
        "symptoms": (
            "Reddish discolouration of internal stalk tissue with white spots. "
            "Leaves show yellowing, then drying from tips. Rotting stalk emits alcohol-like smell."
        ),
        "causes": (
            "Caused by Colletotrichum falcatum. "
            "Spreads through infected setts and crop residue. "
            "Favoured by high rainfall and waterlogging."
        ),
        "prevention": (
            "Plant disease-free, certified healthy setts. "
            "Use resistant varieties. "
            "Treat setts with hot water (50 °C for 2 hours) before planting. "
            "Avoid waterlogged conditions."
        ),
        "treatment": (
            "No curative treatment once disease is established. "
            "Destroy infected clumps. "
            "Treat setts with Carbendazim 0.1% (1 g/litre) before planting."
        ),
        "pesticides": [
            {
                "name": "Carbendazim 50% WP (Sett Treatment)",
                "pesticide_type": "fungicide",
                "active_ingredient": "Carbendazim",
                "dosage": "1 g per litre of water; soak setts for 15–30 minutes",
                "application_method": "Sett soaking before planting. Allows thorough penetration.",
                "safety_notes": "Use gloves and eye protection during mixing. Treated setts not for consumption.",
            },
        ],
    },
    {
        "crop_name": "Onion",
        "disease_name": "Purple Blotch",
        "severity": "medium",
        "symptoms": (
            "Small whitish lesions that enlarge with a purple centre surrounded by a yellow halo. "
            "Lesions coalesce causing stem collapse. Severely infected plants lodge at neck."
        ),
        "causes": (
            "Caused by Alternaria porri. "
            "Favoured by warm (21–30 °C), humid weather. Spreads via airborne conidia."
        ),
        "prevention": (
            "Use disease-free transplants. "
            "Avoid overhead irrigation. "
            "Maintain adequate spacing for air circulation. "
            "Practice crop rotation."
        ),
        "treatment": (
            "Apply Iprodione 50% WP at 2 g/litre or Mancozeb 75% WP at 2 g/litre. "
            "Begin sprays preventively; repeat every 7–10 days."
        ),
        "pesticides": [
            {
                "name": "Iprodione 50% WP",
                "pesticide_type": "fungicide",
                "active_ingredient": "Iprodione",
                "dosage": "2 g per litre of water; 200 litres/ha",
                "application_method": "Foliar spray. Start before disease onset. Repeat every 7–10 days.",
                "safety_notes": "Avoid skin and eye contact. PHI: 21 days.",
            },
        ],
    },
    {
        "crop_name": "Soybean",
        "disease_name": "Soybean Mosaic Virus",
        "severity": "medium",
        "symptoms": (
            "Mosaic pattern of light and dark green on leaves, leaf puckering, and curling. "
            "Stunted plant growth. Pods may be distorted or fewer seeds produced."
        ),
        "causes": (
            "Soybean Mosaic Virus (SMV) transmitted by aphids (especially Aphis glycines). "
            "Also spread through infected seed."
        ),
        "prevention": (
            "Plant certified virus-free seed. "
            "Control aphid vectors using systemic insecticides at early growth stages. "
            "Remove infected plants promptly. Use resistant varieties."
        ),
        "treatment": (
            "No direct curative treatment for the virus. "
            "Control aphid vector with Imidacloprid 17.8% SL at 0.3 ml/litre. "
            "Remove and destroy severely infected plants."
        ),
        "pesticides": [
            {
                "name": "Imidacloprid 17.8% SL",
                "pesticide_type": "insecticide",
                "active_ingredient": "Imidacloprid",
                "dosage": "0.3 ml per litre of water; 200 litres/ha",
                "application_method": "Foliar spray targeting aphid colonies. Cover leaf undersides well.",
                "safety_notes": "Highly toxic to bees. Do not spray during flowering. PHI: 7 days.",
            },
        ],
    },
]


MARKET_PRICE_DATA = [
    {"crop_name": "Rice (Basmati)", "market_name": "Azadpur Mandi", "location": "Delhi", "price": 3500, "unit": "per_quintal", "date": date(2026, 9, 20)},
    {"crop_name": "Wheat", "market_name": "Nafed Mandi", "location": "Indore, MP", "price": 2200, "unit": "per_quintal", "date": date(2026, 9, 20)},
    {"crop_name": "Tomato", "market_name": "Vashi APMC", "location": "Navi Mumbai, MH", "price": 35, "unit": "per_kg", "date": date(2026, 9, 20)},
    {"crop_name": "Potato", "market_name": "Azadpur Mandi", "location": "Delhi", "price": 22, "unit": "per_kg", "date": date(2026, 9, 21)},
    {"crop_name": "Onion", "market_name": "Lasalgaon APMC", "location": "Nashik, MH", "price": 18, "unit": "per_kg", "date": date(2026, 9, 21)},
    {"crop_name": "Maize", "market_name": "Gulbarga Market", "location": "Gulbarga, KA", "price": 1850, "unit": "per_quintal", "date": date(2026, 9, 19)},
    {"crop_name": "Cotton", "market_name": "Yavatmal Mandi", "location": "Yavatmal, MH", "price": 6500, "unit": "per_quintal", "date": date(2026, 9, 18)},
    {"crop_name": "Sugarcane", "market_name": "Kolhapur Sugar Mill", "location": "Kolhapur, MH", "price": 340, "unit": "per_quintal", "date": date(2026, 9, 15)},
    {"crop_name": "Groundnut", "market_name": "Rajkot Market", "location": "Rajkot, GJ", "price": 5800, "unit": "per_quintal", "date": date(2026, 9, 22)},
    {"crop_name": "Soybean", "market_name": "Indore Mandi", "location": "Indore, MP", "price": 4400, "unit": "per_quintal", "date": date(2026, 9, 22)},
    {"crop_name": "Chickpea", "market_name": "Bikaner Mandi", "location": "Bikaner, RJ", "price": 5200, "unit": "per_quintal", "date": date(2026, 9, 17)},
    {"crop_name": "Bajra", "market_name": "Jodhpur Mandi", "location": "Jodhpur, RJ", "price": 2100, "unit": "per_quintal", "date": date(2026, 9, 16)},
]

SOIL_SAMPLE_DATA = [
    {
        'soil_type': 'loamy', 'ph': 6.5, 'nitrogen': 180.0, 'phosphorus': 38.0, 'potassium': 90.0,
        'moisture': 28.0, 'organic_matter': 2.8, 'notes': 'DEMO SAMPLE DATA — not real field data.'
    },
    {
        'soil_type': 'clay', 'ph': 7.1, 'nitrogen': 210.0, 'phosphorus': 42.0, 'potassium': 105.0,
        'moisture': 35.0, 'organic_matter': 3.2, 'notes': 'DEMO SAMPLE DATA — not real field data.'
    },
    {
        'soil_type': 'sandy', 'ph': 6.0, 'nitrogen': 150.0, 'phosphorus': 24.0, 'potassium': 58.0,
        'moisture': 18.0, 'organic_matter': 1.7, 'notes': 'DEMO SAMPLE DATA — not real field data.'
    },
    {
        'soil_type': 'black', 'ph': 7.8, 'nitrogen': 220.0, 'phosphorus': 32.0, 'potassium': 120.0,
        'moisture': 31.0, 'organic_matter': 3.6, 'notes': 'DEMO SAMPLE DATA — not real field data.'
    },
    {
        'soil_type': 'loamy', 'ph': 5.9, 'nitrogen': 170.0, 'phosphorus': 28.0, 'potassium': 78.0,
        'moisture': 26.0, 'organic_matter': 2.5, 'notes': 'DEMO SAMPLE DATA — not real field data.'
    },
]

CROP_SAMPLE_DATA = [
    {'crop_name': 'Rice', 'crop_type': 'cereal', 'variety': 'Pusa Basmati 1121', 'land_area': '5.0', 'area_unit': 'acres', 'soil_type': 'loamy', 'irrigation_type': 'canal', 'status': 'growing', 'notes': 'DEMO SAMPLE DATA — not real field data.'},
    {'crop_name': 'Wheat', 'crop_type': 'cereal', 'variety': 'HD 2967', 'land_area': '3.5', 'area_unit': 'acres', 'soil_type': 'clay', 'irrigation_type': 'sprinkler', 'status': 'planned', 'notes': 'DEMO SAMPLE DATA — not real field data.'},
    {'crop_name': 'Tomato', 'crop_type': 'vegetable', 'variety': 'Arka Samrat', 'land_area': '1.5', 'area_unit': 'acres', 'soil_type': 'sandy', 'irrigation_type': 'drip', 'status': 'ready', 'notes': 'DEMO SAMPLE DATA — not real field data.'},
    {'crop_name': 'Cotton', 'crop_type': 'cash_crop', 'variety': 'BG II', 'land_area': '4.0', 'area_unit': 'acres', 'soil_type': 'black', 'irrigation_type': 'well', 'status': 'harvested', 'notes': 'DEMO SAMPLE DATA — not real field data.'},
]


class Command(BaseCommand):
    help = (
        "Load demo-only sample data for soil, crops, diseases, pesticides, and market prices. "
        "This data is for demonstration purposes only and not real farm data."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            '--catalog-only',
            action='store_true',
            help='Load shared disease and market catalogs without creating farmer demo records.',
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Remove existing demo sample data before loading new data.',
        )

    def handle(self, *args, **options):
        if options['catalog_only'] and options['clear']:
            raise CommandError('--clear cannot be combined with --catalog-only.')

        if options['clear']:
            self.stdout.write("Clearing existing demo sample data...")
            Crop.objects.filter(is_sample_data=True).delete()
            SoilData.objects.filter(is_sample_data=True).delete()
            MarketPrice.objects.filter(is_sample_data=True).delete()
            Disease.objects.all().delete()
            self.stdout.write(self.style.WARNING("Existing sample data cleared."))

        farmers = [] if options['catalog_only'] else list(User.objects.order_by('id'))
        if not farmers and not options['catalog_only']:
            farmers = [
                User.objects.create_user(username='demo_farmer_1', email='demo1@example.com', password='DemoPass123!'),
                User.objects.create_user(username='demo_farmer_2', email='demo2@example.com', password='DemoPass123!'),
            ]

        self.stdout.write("\nLoading demo soil and crop data...")
        soil_count = 0
        crop_count = 0
        for farmer in farmers[:2]:
            for sample in SOIL_SAMPLE_DATA:
                soil, created = SoilData.objects.get_or_create(
                    farmer=farmer,
                    soil_type=sample['soil_type'],
                    ph=sample['ph'],
                    nitrogen=sample['nitrogen'],
                    phosphorus=sample['phosphorus'],
                    potassium=sample['potassium'],
                    defaults={**sample, 'is_sample_data': True},
                )
                if created:
                    soil_count += 1
                    soil.is_sample_data = True
                    soil.notes = 'DEMO SAMPLE DATA — not real field data.'
                    soil.save(update_fields=['is_sample_data', 'notes'])

            for sample in CROP_SAMPLE_DATA:
                crop, created = Crop.objects.get_or_create(
                    farmer=farmer,
                    crop_name=sample['crop_name'],
                    variety=sample['variety'],
                    defaults={**sample, 'land_area': sample['land_area'], 'is_sample_data': True},
                )
                if created:
                    crop_count += 1
                    crop.is_sample_data = True
                    crop.notes = 'DEMO SAMPLE DATA — not real field data.'
                    crop.save(update_fields=['is_sample_data', 'notes', 'status'])

        self.stdout.write("\nLoading disease and pesticide data...")
        disease_count = 0
        pesticide_count = 0
        for d in DISEASE_DATA:
            pesticides = d.pop("pesticides", [])
            disease, created = Disease.objects.get_or_create(
                crop_name=d["crop_name"],
                disease_name=d["disease_name"],
                defaults=d,
            )
            if created:
                disease_count += 1
                for p in pesticides:
                    Pesticide.objects.create(disease=disease, **p)
                    pesticide_count += 1

        self.stdout.write("Loading sample market price data...")
        market_count = 0
        for mp in MARKET_PRICE_DATA:
            _, created = MarketPrice.objects.get_or_create(
                crop_name=mp["crop_name"],
                market_name=mp["market_name"],
                date=mp["date"],
                defaults={**mp, "is_sample_data": True},
            )
            if created:
                market_count += 1

        self.stdout.write(self.style.SUCCESS(
            f"\n[OK] Demo sample data loaded successfully!\n"
            f"  Soil records: {soil_count} added\n"
            f"  Crop records: {crop_count} added\n"
            f"  Diseases: {disease_count} added\n"
            f"  Pesticides: {pesticide_count} added\n"
            f"  Market prices: {market_count} added\n"
            f"\nNOTE: This is demo/sample data for portfolio demonstration only.\n"
            f"   Please do not treat these as live farm data or production records."
        ))
