from model import PlaceModel


PLACES_DATABASE = {

    "goa": [
        PlaceModel(
            name="Baga Beach",
            description="Popular beach known for water sports, nightlife, and beach shacks.",
            location="North Goa",
            category="Beach",
            rating=4.3,
            estimated_time_hours=3.0,
            entry_fee=None
        ),
        PlaceModel(
            name="Calangute Beach",
            description="One of Goa's most famous beaches with restaurants and water activities.",
            location="North Goa",
            category="Beach",
            rating=4.2,
            estimated_time_hours=3.0,
            entry_fee=None
        ),
        PlaceModel(
            name="Fort Aguada",
            description="Historic Portuguese fort with beautiful views of the Arabian Sea.",
            location="Candolim, North Goa",
            category="Historical",
            rating=4.5,
            estimated_time_hours=2.0,
            entry_fee=50.0
        ),
        PlaceModel(
            name="Basilica of Bom Jesus",
            description="Historic church and UNESCO World Heritage Site.",
            location="Old Goa",
            category="Religious",
            rating=4.5,
            estimated_time_hours=1.5,
            entry_fee=None
        ),
        PlaceModel(
            name="Dudhsagar Waterfalls",
            description="Spectacular four-tiered waterfall surrounded by lush forest.",
            location="Mollem, Goa",
            category="Nature",
            rating=4.7,
            estimated_time_hours=6.0,
            entry_fee=400.0
        ),
        PlaceModel(
            name="Anjuna Beach",
            description="Scenic beach famous for its relaxed atmosphere and flea market.",
            location="North Goa",
            category="Beach",
            rating=4.3,
            estimated_time_hours=3.0,
            entry_fee=None
        ),
        PlaceModel(
            name="Chapora Fort",
            description="Historic fort offering panoramic views of the coastline.",
            location="Chapora, North Goa",
            category="Historical",
            rating=4.4,
            estimated_time_hours=2.0,
            entry_fee=None
        ),
        PlaceModel(
            name="Palolem Beach",
            description="Beautiful crescent-shaped beach with a peaceful atmosphere.",
            location="South Goa",
            category="Beach",
            rating=4.6,
            estimated_time_hours=3.0,
            entry_fee=None
        ),
        PlaceModel(
            name="Spice Plantation",
            description="Traditional spice farm experience surrounded by tropical greenery.",
            location="Ponda, Goa",
            category="Nature",
            rating=4.4,
            estimated_time_hours=3.0,
            entry_fee=500.0
        ),
        PlaceModel(
            name="Fontainhas",
            description="Colorful Latin Quarter known for Portuguese-style houses.",
            location="Panaji, Goa",
            category="Culture",
            rating=4.5,
            estimated_time_hours=2.0,
            entry_fee=None
        ),
    ],

    "delhi": [
        PlaceModel(
            name="India Gate",
            description="Iconic war memorial and one of Delhi's most recognizable landmarks.",
            location="New Delhi",
            category="Historical",
            rating=4.6,
            estimated_time_hours=2.0,
            entry_fee=None
        ),
        PlaceModel(
            name="Red Fort",
            description="Historic Mughal fort and UNESCO World Heritage Site.",
            location="Old Delhi",
            category="Historical",
            rating=4.5,
            estimated_time_hours=3.0,
            entry_fee=35.0
        ),
        PlaceModel(
            name="Qutub Minar",
            description="Historic 73-meter tall minaret and UNESCO World Heritage Site.",
            location="Mehrauli, Delhi",
            category="Historical",
            rating=4.6,
            estimated_time_hours=2.5,
            entry_fee=35.0
        ),
        PlaceModel(
            name="Lotus Temple",
            description="Beautiful Bahá'í House of Worship famous for its lotus-shaped architecture.",
            location="South Delhi",
            category="Religious",
            rating=4.5,
            estimated_time_hours=1.5,
            entry_fee=None
        ),
        PlaceModel(
            name="Humayun's Tomb",
            description="Magnificent Mughal-era tomb surrounded by beautiful gardens.",
            location="Nizamuddin, Delhi",
            category="Historical",
            rating=4.6,
            estimated_time_hours=2.0,
            entry_fee=35.0
        ),
        PlaceModel(
            name="Akshardham Temple",
            description="Large Hindu temple complex featuring impressive architecture and exhibitions.",
            location="East Delhi",
            category="Religious",
            rating=4.7,
            estimated_time_hours=4.0,
            entry_fee=None
        ),
        PlaceModel(
            name="Jama Masjid",
            description="One of India's largest and most famous mosques.",
            location="Old Delhi",
            category="Religious",
            rating=4.5,
            estimated_time_hours=1.5,
            entry_fee=None
        ),
        PlaceModel(
            name="Chandni Chowk",
            description="Historic market famous for street food, shopping, and Old Delhi culture.",
            location="Old Delhi",
            category="Shopping",
            rating=4.4,
            estimated_time_hours=3.0,
            entry_fee=None
        ),
        PlaceModel(
            name="Lodhi Garden",
            description="Peaceful garden containing historic tombs and monuments.",
            location="Central Delhi",
            category="Nature",
            rating=4.6,
            estimated_time_hours=2.0,
            entry_fee=None
        ),
        PlaceModel(
            name="National Museum",
            description="Major museum showcasing Indian history, art, and archaeology.",
            location="New Delhi",
            category="Museum",
            rating=4.4,
            estimated_time_hours=3.0,
            entry_fee=20.0
        ),
    ],

    "jaipur": [
        PlaceModel(
            name="Amber Fort",
            description="Magnificent hilltop fort known for Rajput architecture and courtyards.",
            location="Amer, Jaipur",
            category="Historical",
            rating=4.7,
            estimated_time_hours=3.0,
            entry_fee=100.0
        ),
        PlaceModel(
            name="Hawa Mahal",
            description="Iconic pink sandstone palace famous for its honeycomb windows.",
            location="Jaipur",
            category="Historical",
            rating=4.6,
            estimated_time_hours=1.5,
            entry_fee=50.0
        ),
        PlaceModel(
            name="City Palace",
            description="Royal palace complex showcasing Jaipur's royal heritage.",
            location="Jaipur",
            category="Historical",
            rating=4.6,
            estimated_time_hours=2.5,
            entry_fee=200.0
        ),
        PlaceModel(
            name="Jantar Mantar",
            description="Historic astronomical observatory featuring massive scientific instruments.",
            location="Jaipur",
            category="Science",
            rating=4.5,
            estimated_time_hours=1.5,
            entry_fee=50.0
        ),
        PlaceModel(
            name="Jal Mahal",
            description="Beautiful palace located in the middle of Man Sagar Lake.",
            location="Jaipur",
            category="Historical",
            rating=4.4,
            estimated_time_hours=1.0,
            entry_fee=None
        ),
        PlaceModel(
            name="Nahargarh Fort",
            description="Hilltop fort offering spectacular panoramic views of Jaipur.",
            location="Aravalli Hills, Jaipur",
            category="Historical",
            rating=4.5,
            estimated_time_hours=2.5,
            entry_fee=50.0
        ),
        PlaceModel(
            name="Jaigarh Fort",
            description="Historic fort famous for its massive cannon and hilltop views.",
            location="Amer, Jaipur",
            category="Historical",
            rating=4.5,
            estimated_time_hours=2.5,
            entry_fee=100.0
        ),
        PlaceModel(
            name="Albert Hall Museum",
            description="Historic museum displaying art, artifacts, and cultural collections.",
            location="Jaipur",
            category="Museum",
            rating=4.4,
            estimated_time_hours=2.0,
            entry_fee=40.0
        ),
        PlaceModel(
            name="Birla Mandir",
            description="Beautiful white marble Hindu temple dedicated to Lord Vishnu and Goddess Lakshmi.",
            location="Jaipur",
            category="Religious",
            rating=4.6,
            estimated_time_hours=1.5,
            entry_fee=None
        ),
        PlaceModel(
            name="Chokhi Dhani",
            description="Cultural village experience showcasing traditional Rajasthani food, music, and performances.",
            location="Jaipur",
            category="Culture",
            rating=4.4,
            estimated_time_hours=4.0,
            entry_fee=800.0
        ),
    ],
}


async def fetch_places(destination:str)->list[PlaceModel]:
    """ Fetch places of intrest for a given destination."""
    
    return PLACES_DATABASE.get(destination.lower(),[])