export interface CountryData {
  code: string;
  name: string;
  states?: StateData[];
}

export interface StateData {
  code: string;
  name: string;
}

export const countries: CountryData[] = [
  {
    code: "afghanistan",
    name: "Afghanistan",
    states: [
      { code: "kabul", name: "Kabul" },
      { code: "kandahar", name: "Kandahar" },
      { code: "herat", name: "Herat" },
      { code: "balkh", name: "Balkh" }
    ]
  },
  {
    code: "albania",
    name: "Albania",
    states: [
      { code: "tirana", name: "Tirana" },
      { code: "durres", name: "Durrës" },
      { code: "vlore", name: "Vlorë" },
      { code: "shkoder", name: "Shkodër" }
    ]
  },
  {
    code: "algeria",
    name: "Algeria",
    states: [
      { code: "algiers", name: "Algiers" },
      { code: "oran", name: "Oran" },
      { code: "constantine", name: "Constantine" },
      { code: "annaba", name: "Annaba" }
    ]
  },
  {
    code: "argentina",
    name: "Argentina",
    states: [
      { code: "buenos-aires", name: "Buenos Aires" },
      { code: "cordoba", name: "Córdoba" },
      { code: "santa-fe", name: "Santa Fe" },
      { code: "mendoza", name: "Mendoza" }
    ]
  },
  {
    code: "australia",
    name: "Australia",
    states: [
      { code: "new-south-wales", name: "New South Wales" },
      { code: "victoria", name: "Victoria" },
      { code: "queensland", name: "Queensland" },
      { code: "western-australia", name: "Western Australia" },
      { code: "south-australia", name: "South Australia" },
      { code: "tasmania", name: "Tasmania" },
      { code: "northern-territory", name: "Northern Territory" },
      { code: "australian-capital-territory", name: "Australian Capital Territory" }
    ]
  },
  {
    code: "austria",
    name: "Austria",
    states: [
      { code: "vienna", name: "Vienna" },
      { code: "lower-austria", name: "Lower Austria" },
      { code: "upper-austria", name: "Upper Austria" },
      { code: "styria", name: "Styria" },
      { code: "tyrol", name: "Tyrol" },
      { code: "carinthia", name: "Carinthia" },
      { code: "salzburg", name: "Salzburg" },
      { code: "vorarlberg", name: "Vorarlberg" },
      { code: "burgenland", name: "Burgenland" }
    ]
  },
  {
    code: "bangladesh",
    name: "Bangladesh",
    states: [
      { code: "dhaka", name: "Dhaka" },
      { code: "chittagong", name: "Chittagong" },
      { code: "rajshahi", name: "Rajshahi" },
      { code: "khulna", name: "Khulna" },
      { code: "sylhet", name: "Sylhet" },
      { code: "barisal", name: "Barisal" },
      { code: "rangpur", name: "Rangpur" },
      { code: "mymensingh", name: "Mymensingh" }
    ]
  },
  {
    code: "belgium",
    name: "Belgium",
    states: [
      { code: "flanders", name: "Flanders" },
      { code: "wallonia", name: "Wallonia" },
      { code: "brussels", name: "Brussels-Capital Region" }
    ]
  },
  {
    code: "brazil",
    name: "Brazil",
    states: [
      { code: "sao-paulo", name: "São Paulo" },
      { code: "rio-de-janeiro", name: "Rio de Janeiro" },
      { code: "minas-gerais", name: "Minas Gerais" },
      { code: "bahia", name: "Bahia" },
      { code: "parana", name: "Paraná" },
      { code: "rio-grande-do-sul", name: "Rio Grande do Sul" },
      { code: "pernambuco", name: "Pernambuco" },
      { code: "ceara", name: "Ceará" }
    ]
  },
  {
    code: "canada",
    name: "Canada",
    states: [
      { code: "ontario", name: "Ontario" },
      { code: "quebec", name: "Quebec" },
      { code: "british-columbia", name: "British Columbia" },
      { code: "alberta", name: "Alberta" },
      { code: "manitoba", name: "Manitoba" },
      { code: "saskatchewan", name: "Saskatchewan" },
      { code: "nova-scotia", name: "Nova Scotia" },
      { code: "new-brunswick", name: "New Brunswick" },
      { code: "newfoundland-and-labrador", name: "Newfoundland and Labrador" },
      { code: "prince-edward-island", name: "Prince Edward Island" },
      { code: "northwest-territories", name: "Northwest Territories" },
      { code: "yukon", name: "Yukon" },
      { code: "nunavut", name: "Nunavut" }
    ]
  },
  {
    code: "china",
    name: "China",
    states: [
      { code: "beijing", name: "Beijing" },
      { code: "shanghai", name: "Shanghai" },
      { code: "guangdong", name: "Guangdong" },
      { code: "shandong", name: "Shandong" },
      { code: "henan", name: "Henan" },
      { code: "sichuan", name: "Sichuan" },
      { code: "jiangsu", name: "Jiangsu" },
      { code: "hebei", name: "Hebei" }
    ]
  },
  {
    code: "denmark",
    name: "Denmark",
    states: [
      { code: "capital-region", name: "Capital Region" },
      { code: "central-jutland", name: "Central Jutland" },
      { code: "north-jutland", name: "North Jutland" },
      { code: "zealand", name: "Zealand" },
      { code: "southern-denmark", name: "Southern Denmark" }
    ]
  },
  {
    code: "egypt",
    name: "Egypt",
    states: [
      { code: "cairo", name: "Cairo" },
      { code: "alexandria", name: "Alexandria" },
      { code: "giza", name: "Giza" },
      { code: "luxor", name: "Luxor" }
    ]
  },
  {
    code: "finland",
    name: "Finland",
    states: [
      { code: "uusimaa", name: "Uusimaa" },
      { code: "pirkanmaa", name: "Pirkanmaa" },
      { code: "varsinais-suomi", name: "Varsinais-Suomi" },
      { code: "pohjois-pohjanmaa", name: "Pohjois-Pohjanmaa" }
    ]
  },
  {
    code: "france",
    name: "France",
    states: [
      { code: "ile-de-france", name: "Île-de-France" },
      { code: "auvergne-rhone-alpes", name: "Auvergne-Rhône-Alpes" },
      { code: "hauts-de-france", name: "Hauts-de-France" },
      { code: "nouvelle-aquitaine", name: "Nouvelle-Aquitaine" },
      { code: "occitanie", name: "Occitanie" },
      { code: "grand-est", name: "Grand Est" },
      { code: "provence-alpes-cote-d-azur", name: "Provence-Alpes-Côte d'Azur" },
      { code: "pays-de-la-loire", name: "Pays de la Loire" }
    ]
  },
  {
    code: "germany",
    name: "Germany",
    states: [
      { code: "north-rhine-westphalia", name: "North Rhine-Westphalia" },
      { code: "bavaria", name: "Bavaria" },
      { code: "baden-württemberg", name: "Baden-Württemberg" },
      { code: "lower-saxony", name: "Lower Saxony" },
      { code: "hesse", name: "Hesse" },
      { code: "saxony", name: "Saxony" },
      { code: "rhineland-palatinate", name: "Rhineland-Palatinate" },
      { code: "berlin", name: "Berlin" },
      { code: "schleswig-holstein", name: "Schleswig-Holstein" },
      { code: "brandenburg", name: "Brandenburg" },
      { code: "saxony-anhalt", name: "Saxony-Anhalt" },
      { code: "thuringia", name: "Thuringia" },
      { code: "hamburg", name: "Hamburg" },
      { code: "mecklenburg-vorpommern", name: "Mecklenburg-Vorpommern" },
      { code: "saarland", name: "Saarland" },
      { code: "bremen", name: "Bremen" }
    ]
  },
  {
    code: "greece",
    name: "Greece",
    states: [
      { code: "attica", name: "Attica" },
      { code: "central-macedonia", name: "Central Macedonia" },
      { code: "thessaly", name: "Thessaly" },
      { code: "crete", name: "Crete" }
    ]
  },
  {
    code: "india",
    name: "India",
    states: [
      { code: "uttar-pradesh", name: "Uttar Pradesh" },
      { code: "maharashtra", name: "Maharashtra" },
      { code: "bihar", name: "Bihar" },
      { code: "west-bengal", name: "West Bengal" },
      { code: "madhya-pradesh", name: "Madhya Pradesh" },
      { code: "tamil-nadu", name: "Tamil Nadu" },
      { code: "rajasthan", name: "Rajasthan" },
      { code: "karnataka", name: "Karnataka" },
      { code: "gujarat", name: "Gujarat" },
      { code: "andhra-pradesh", name: "Andhra Pradesh" },
      { code: "odisha", name: "Odisha" },
      { code: "telangana", name: "Telangana" },
      { code: "kerala", name: "Kerala" },
      { code: "jharkhand", name: "Jharkhand" },
      { code: "assam", name: "Assam" },
      { code: "punjab", name: "Punjab" },
      { code: "haryana", name: "Haryana" },
      { code: "chhattisgarh", name: "Chhattisgarh" },
      { code: "jammu-and-kashmir", name: "Jammu and Kashmir" },
      { code: "uttarakhand", name: "Uttarakhand" },
      { code: "himachal-pradesh", name: "Himachal Pradesh" },
      { code: "tripura", name: "Tripura" },
      { code: "meghalaya", name: "Meghalaya" },
      { code: "manipur", name: "Manipur" },
      { code: "nagaland", name: "Nagaland" },
      { code: "goa", name: "Goa" },
      { code: "arunachal-pradesh", name: "Arunachal Pradesh" },
      { code: "mizoram", name: "Mizoram" },
      { code: "sikkim", name: "Sikkim" },
      { code: "delhi", name: "Delhi" },
      { code: "puducherry", name: "Puducherry" },
      { code: "chandigarh", name: "Chandigarh" },
      { code: "andaman-and-nicobar", name: "Andaman and Nicobar Islands" },
      { code: "dadra-and-nagar-haveli", name: "Dadra and Nagar Haveli" },
      { code: "daman-and-diu", name: "Daman and Diu" },
      { code: "lakshadweep", name: "Lakshadweep" },
      { code: "ladakh", name: "Ladakh" }
    ]
  },
  {
    code: "indonesia",
    name: "Indonesia",
    states: [
      { code: "jakarta", name: "Jakarta" },
      { code: "west-java", name: "West Java" },
      { code: "east-java", name: "East Java" },
      { code: "central-java", name: "Central Java" },
      { code: "sumatra", name: "Sumatra" },
      { code: "bali", name: "Bali" }
    ]
  },
  {
    code: "ireland",
    name: "Ireland",
    states: [
      { code: "leinster", name: "Leinster" },
      { code: "munster", name: "Munster" },
      { code: "connacht", name: "Connacht" },
      { code: "ulster", name: "Ulster" }
    ]
  },
  {
    code: "italy",
    name: "Italy",
    states: [
      { code: "lombardy", name: "Lombardy" },
      { code: "lazio", name: "Lazio" },
      { code: "campania", name: "Campania" },
      { code: "sicily", name: "Sicily" },
      { code: "veneto", name: "Veneto" },
      { code: "emilia-romagna", name: "Emilia-Romagna" },
      { code: "piedmont", name: "Piedmont" },
      { code: "puglia", name: "Puglia" },
      { code: "tuscany", name: "Tuscany" },
      { code: "calabria", name: "Calabria" }
    ]
  },
  {
    code: "japan",
    name: "Japan",
    states: [
      { code: "tokyo", name: "Tokyo" },
      { code: "osaka", name: "Osaka" },
      { code: "kanagawa", name: "Kanagawa" },
      { code: "aichi", name: "Aichi" },
      { code: "saitama", name: "Saitama" },
      { code: "chiba", name: "Chiba" },
      { code: "hyogo", name: "Hyogo" },
      { code: "hokkaido", name: "Hokkaido" },
      { code: "fukuoka", name: "Fukuoka" },
      { code: "shizuoka", name: "Shizuoka" }
    ]
  },
  {
    code: "kazakhstan",
    name: "Kazakhstan",
    states: [
      { code: "almaty", name: "Almaty" },
      { code: "nur-sultan", name: "Nur-Sultan" },
      { code: "shymkent", name: "Shymkent" },
      { code: "aktobe", name: "Aktobe" }
    ]
  },
  {
    code: "kenya",
    name: "Kenya",
    states: [
      { code: "nairobi", name: "Nairobi" },
      { code: "mombasa", name: "Mombasa" },
      { code: "nakuru", name: "Nakuru" },
      { code: "eldoret", name: "Eldoret" }
    ]
  },
  {
    code: "mexico",
    name: "Mexico",
    states: [
      { code: "mexico-city", name: "Mexico City" },
      { code: "jalisco", name: "Jalisco" },
      { code: "nuevo-leon", name: "Nuevo León" },
      { code: "puebla", name: "Puebla" },
      { code: "guanajuato", name: "Guanajuato" },
      { code: "chihuahua", name: "Chihuahua" },
      { code: "baja-california", name: "Baja California" },
      { code: "veracruz", name: "Veracruz" }
    ]
  },
  {
    code: "mongolia",
    name: "Mongolia",
    states: [
      { code: "ulaanbaatar", name: "Ulaanbaatar" },
      { code: "darkhan-uul", name: "Darkhan-Uul" },
      { code: "erdenet", name: "Erdenet" },
      { code: "umnugovi", name: "Ömnögovi" }
    ]
  },
  {
    code: "netherlands",
    name: "Netherlands",
    states: [
      { code: "north-holland", name: "North Holland" },
      { code: "south-holland", name: "South Holland" },
      { code: "utrecht", name: "Utrecht" },
      { code: "north-brabant", name: "North Brabant" },
      { code: "gelderland", name: "Gelderland" },
      { code: "overijssel", name: "Overijssel" },
      { code: "groningen", name: "Groningen" },
      { code: "friesland", name: "Friesland" },
      { code: "drenthe", name: "Drenthe" },
      { code: "limburg", name: "Limburg" },
      { code: "zeeland", name: "Zeeland" },
      { code: "flevoland", name: "Flevoland" }
    ]
  },
  {
    code: "new-zealand",
    name: "New Zealand",
    states: [
      { code: "north-island", name: "North Island" },
      { code: "south-island", name: "South Island" },
      { code: "stewart-island", name: "Stewart Island" }
    ]
  },
  {
    code: "nigeria",
    name: "Nigeria",
    states: [
      { code: "lagos", name: "Lagos" },
      { code: "kano", name: "Kano" },
      { code: "kaduna", name: "Kaduna" },
      { code: "rivers", name: "Rivers" },
      { code: "oyo", name: "Oyo" },
      { code: "delta", name: "Delta" }
    ]
  },
  {
    code: "norway",
    name: "Norway",
    states: [
      { code: "oslo", name: "Oslo" },
      { code: "viken", name: "Viken" },
      { code: "vestland", name: "Vestland" },
      { code: "rogaland", name: "Rogaland" },
      { code: "more-og-romsdal", name: "Møre og Romsdal" },
      { code: "nordland", name: "Nordland" },
      { code: "innlandet", name: "Innlandet" },
      { code: "agder", name: "Agder" },
      { code: "vestfold-og-telemark", name: "Vestfold og Telemark" },
      { code: "trondelag", name: "Trøndelag" },
      { code: "troms-og-finnmark", name: "Troms og Finnmark" }
    ]
  },
  {
    code: "pakistan",
    name: "Pakistan",
    states: [
      { code: "punjab", name: "Punjab" },
      { code: "sindh", name: "Sindh" },
      { code: "khyber-pakhtunkhwa", name: "Khyber Pakhtunkhwa" },
      { code: "balochistan", name: "Balochistan" },
      { code: "islamabad", name: "Islamabad Capital Territory" }
    ]
  },
  {
    code: "philippines",
    name: "Philippines",
    states: [
      { code: "metro-manila", name: "Metro Manila" },
      { code: "cebu", name: "Cebu" },
      { code: "davao", name: "Davao" },
      { code: "cagayan-de-oro", name: "Cagayan de Oro" }
    ]
  },
  {
    code: "poland",
    name: "Poland",
    states: [
      { code: "masovian", name: "Masovian" },
      { code: "silesian", name: "Silesian" },
      { code: "lesser-poland", name: "Lesser Poland" },
      { code: "greater-poland", name: "Greater Poland" },
      { code: "lower-silesian", name: "Lower Silesian" },
      { code: "lublin", name: "Lublin" },
      { code: "west-pomeranian", name: "West Pomeranian" },
      { code: "lodz", name: "Łódź" }
    ]
  },
  {
    code: "portugal",
    name: "Portugal",
    states: [
      { code: "lisbon", name: "Lisbon" },
      { code: "porto", name: "Porto" },
      { code: "braga", name: "Braga" },
      { code: "setúbal", name: "Setúbal" },
      { code: "coimbra", name: "Coimbra" }
    ]
  },
  {
    code: "russia",
    name: "Russia",
    states: [
      { code: "moscow", name: "Moscow" },
      { code: "saint-petersburg", name: "Saint Petersburg" },
      { code: "novosibirsk", name: "Novosibirsk" },
      { code: "yekaterinburg", name: "Yekaterinburg" },
      { code: "nizhny-novgorod", name: "Nizhny Novgorod" },
      { code: "kazan", name: "Kazan" },
      { code: "chelyabinsk", name: "Chelyabinsk" },
      { code: "omsk", name: "Omsk" }
    ]
  },
  {
    code: "saudi-arabia",
    name: "Saudi Arabia",
    states: [
      { code: "riyadh", name: "Riyadh" },
      { code: "mecca", name: "Mecca" },
      { code: "medina", name: "Medina" },
      { code: "eastern-province", name: "Eastern Province" }
    ]
  },
  {
    code: "singapore",
    name: "Singapore",
    states: [
      { code: "central", name: "Central" },
      { code: "north", name: "North" },
      { code: "south", name: "South" },
      { code: "east", name: "East" },
      { code: "west", name: "West" }
    ]
  },
  {
    code: "south-africa",
    name: "South Africa",
    states: [
      { code: "gauteng", name: "Gauteng" },
      { code: "kwazulu-natal", name: "KwaZulu-Natal" },
      { code: "western-cape", name: "Western Cape" },
      { code: "eastern-cape", name: "Eastern Cape" },
      { code: "limpopo", name: "Limpopo" },
      { code: "mpumalanga", name: "Mpumalanga" },
      { code: "north-west", name: "North West" },
      { code: "free-state", name: "Free State" },
      { code: "northern-cape", name: "Northern Cape" }
    ]
  },
  {
    code: "south-korea",
    name: "South Korea",
    states: [
      { code: "seoul", name: "Seoul" },
      { code: "busan", name: "Busan" },
      { code: "incheon", name: "Incheon" },
      { code: "daegu", name: "Daegu" },
      { code: "daejeon", name: "Daejeon" },
      { code: "gwangju", name: "Gwangju" },
      { code: "ulsan", name: "Ulsan" },
      { code: "gyeonggi", name: "Gyeonggi" }
    ]
  },
  {
    code: "spain",
    name: "Spain",
    states: [
      { code: "madrid", name: "Madrid" },
      { code: "catalonia", name: "Catalonia" },
      { code: "valencia", name: "Valencia" },
      { code: "andalusia", name: "Andalusia" },
      { code: "galicia", name: "Galicia" },
      { code: "castile-and-leon", name: "Castile and León" },
      { code: "basque-country", name: "Basque Country" },
      { code: "canary-islands", name: "Canary Islands" },
      { code: "castilla-la-mancha", name: "Castilla-La Mancha" },
      { code: "murcia", name: "Murcia" }
    ]
  },
  {
    code: "sweden",
    name: "Sweden",
    states: [
      { code: "stockholm", name: "Stockholm" },
      { code: "vastra-gotaland", name: "Västra Götaland" },
      { code: "skane", name: "Skåne" },
      { code: "ostergotland", name: "Östergötland" },
      { code: "uppsala", name: "Uppsala" },
      { code: "sodermanland", name: "Södermanland" },
      { code: "jonkoping", name: "Jönköping" },
      { code: "halland", name: "Halland" }
    ]
  },
  {
    code: "switzerland",
    name: "Switzerland",
    states: [
      { code: "zurich", name: "Zurich" },
      { code: "bern", name: "Bern" },
      { code: "vaud", name: "Vaud" },
      { code: "aargau", name: "Aargau" },
      { code: "geneva", name: "Geneva" },
      { code: "ticino", name: "Ticino" },
      { code: "basel-land", name: "Basel-Land" },
      { code: "st-gallen", name: "St. Gallen" }
    ]
  },
  {
    code: "thailand",
    name: "Thailand",
    states: [
      { code: "bangkok", name: "Bangkok" },
      { code: "chiang-mai", name: "Chiang Mai" },
      { code: "nonthaburi", name: "Nonthaburi" },
      { code: "khon-kaen", name: "Khon Kaen" },
      { code: "udon-thani", name: "Udon Thani" }
    ]
  },
  {
    code: "turkey",
    name: "Turkey",
    states: [
      { code: "istanbul", name: "Istanbul" },
      { code: "ankara", name: "Ankara" },
      { code: "izmir", name: "İzmir" },
      { code: "bursa", name: "Bursa" },
      { code: "antalya", name: "Antalya" },
      { code: "adana", name: "Adana" }
    ]
  },
  {
    code: "ukraine",
    name: "Ukraine",
    states: [
      { code: "kyiv", name: "Kyiv" },
      { code: "kharkiv", name: "Kharkiv" },
      { code: "odesa", name: "Odesa" },
      { code: "dnipro", name: "Dnipro" },
      { code: "donetsk", name: "Donetsk" },
      { code: "zaporizhzhia", name: "Zaporizhzhia" }
    ]
  },
  {
    code: "united-kingdom",
    name: "United Kingdom",
    states: [
      { code: "england", name: "England" },
      { code: "scotland", name: "Scotland" },
      { code: "wales", name: "Wales" },
      { code: "northern-ireland", name: "Northern Ireland" }
    ]
  },
  {
    code: "united-states",
    name: "United States",
    states: [
      { code: "alabama", name: "Alabama" },
      { code: "alaska", name: "Alaska" },
      { code: "arizona", name: "Arizona" },
      { code: "arkansas", name: "Arkansas" },
      { code: "california", name: "California" },
      { code: "colorado", name: "Colorado" },
      { code: "connecticut", name: "Connecticut" },
      { code: "delaware", name: "Delaware" },
      { code: "florida", name: "Florida" },
      { code: "georgia", name: "Georgia" },
      { code: "hawaii", name: "Hawaii" },
      { code: "idaho", name: "Idaho" },
      { code: "illinois", name: "Illinois" },
      { code: "indiana", name: "Indiana" },
      { code: "iowa", name: "Iowa" },
      { code: "kansas", name: "Kansas" },
      { code: "kentucky", name: "Kentucky" },
      { code: "louisiana", name: "Louisiana" },
      { code: "maine", name: "Maine" },
      { code: "maryland", name: "Maryland" },
      { code: "massachusetts", name: "Massachusetts" },
      { code: "michigan", name: "Michigan" },
      { code: "minnesota", name: "Minnesota" },
      { code: "mississippi", name: "Mississippi" },
      { code: "missouri", name: "Missouri" },
      { code: "montana", name: "Montana" },
      { code: "nebraska", name: "Nebraska" },
      { code: "nevada", name: "Nevada" },
      { code: "new-hampshire", name: "New Hampshire" },
      { code: "new-jersey", name: "New Jersey" },
      { code: "new-mexico", name: "New Mexico" },
      { code: "new-york", name: "New York" },
      { code: "north-carolina", name: "North Carolina" },
      { code: "north-dakota", name: "North Dakota" },
      { code: "ohio", name: "Ohio" },
      { code: "oklahoma", name: "Oklahoma" },
      { code: "oregon", name: "Oregon" },
      { code: "pennsylvania", name: "Pennsylvania" },
      { code: "rhode-island", name: "Rhode Island" },
      { code: "south-carolina", name: "South Carolina" },
      { code: "south-dakota", name: "South Dakota" },
      { code: "tennessee", name: "Tennessee" },
      { code: "texas", name: "Texas" },
      { code: "utah", name: "Utah" },
      { code: "vermont", name: "Vermont" },
      { code: "virginia", name: "Virginia" },
      { code: "washington", name: "Washington" },
      { code: "west-virginia", name: "West Virginia" },
      { code: "wisconsin", name: "Wisconsin" },
      { code: "wyoming", name: "Wyoming" },
      { code: "district-of-columbia", name: "District of Columbia" },
      { code: "puerto-rico", name: "Puerto Rico" },
      { code: "guam", name: "Guam" },
      { code: "us-virgin-islands", name: "U.S. Virgin Islands" },
      { code: "american-samoa", name: "American Samoa" },
      { code: "northern-mariana-islands", name: "Northern Mariana Islands" }
    ]
  },
  {
    code: "venezuela",
    name: "Venezuela",
    states: [
      { code: "caracas", name: "Caracas" },
      { code: "zulia", name: "Zulia" },
      { code: "miranda", name: "Miranda" },
      { code: "lara", name: "Lara" },
      { code: "carabobo", name: "Carabobo" }
    ]
  },
  {
    code: "vietnam",
    name: "Vietnam",
    states: [
      { code: "ho-chi-minh-city", name: "Ho Chi Minh City" },
      { code: "hanoi", name: "Hanoi" },
      { code: "hai-phong", name: "Hai Phong" },
      { code: "da-nang", name: "Da Nang" },
      { code: "can-tho", name: "Can Tho" }
    ]
  },
  // Additional African Countries
  {
    code: "morocco",
    name: "Morocco",
    states: [
      { code: "casablanca-settat", name: "Casablanca-Settat" },
      { code: "rabat-sale-kenitra", name: "Rabat-Salé-Kénitra" },
      { code: "fes-meknes", name: "Fès-Meknès" },
      { code: "marrakesh-safi", name: "Marrakesh-Safi" },
      { code: "oriental", name: "Oriental" },
      { code: "tangier-tetouan-al-hoceima", name: "Tangier-Tetouan-Al Hoceima" }
    ]
  },
  {
    code: "tunisia",
    name: "Tunisia",
    states: [
      { code: "tunis", name: "Tunis" },
      { code: "sfax", name: "Sfax" },
      { code: "sousse", name: "Sousse" },
      { code: "kairouan", name: "Kairouan" },
      { code: "bizerte", name: "Bizerte" }
    ]
  },
  {
    code: "libya",
    name: "Libya",
    states: [
      { code: "tripoli", name: "Tripoli" },
      { code: "benghazi", name: "Benghazi" },
      { code: "misrata", name: "Misrata" },
      { code: "bayda", name: "Bayda" }
    ]
  },
  {
    code: "sudan",
    name: "Sudan",
    states: [
      { code: "khartoum", name: "Khartoum" },
      { code: "gezira", name: "Gezira" },
      { code: "kassala", name: "Kassala" },
      { code: "red-sea", name: "Red Sea" }
    ]
  },
  {
    code: "ethiopia",
    name: "Ethiopia",
    states: [
      { code: "addis-ababa", name: "Addis Ababa" },
      { code: "oromia", name: "Oromia" },
      { code: "amhara", name: "Amhara" },
      { code: "tigray", name: "Tigray" },
      { code: "southern-nations", name: "Southern Nations, Nationalities, and Peoples" }
    ]
  },
  {
    code: "ghana",
    name: "Ghana",
    states: [
      { code: "greater-accra", name: "Greater Accra" },
      { code: "ashanti", name: "Ashanti" },
      { code: "western", name: "Western" },
      { code: "eastern", name: "Eastern" },
      { code: "central", name: "Central" },
      { code: "volta", name: "Volta" }
    ]
  },
  {
    code: "tanzania",
    name: "Tanzania",
    states: [
      { code: "dar-es-salaam", name: "Dar es Salaam" },
      { code: "mwanza", name: "Mwanza" },
      { code: "arusha", name: "Arusha" },
      { code: "dodoma", name: "Dodoma" },
      { code: "mbeya", name: "Mbeya" }
    ]
  },
  {
    code: "uganda",
    name: "Uganda",
    states: [
      { code: "kampala", name: "Kampala" },
      { code: "wakiso", name: "Wakiso" },
      { code: "mukono", name: "Mukono" },
      { code: "gulu", name: "Gulu" },
      { code: "lira", name: "Lira" }
    ]
  },
  // Asian Countries
  {
    code: "iran",
    name: "Iran",
    states: [
      { code: "tehran", name: "Tehran" },
      { code: "isfahan", name: "Isfahan" },
      { code: "mashhad", name: "Mashhad" },
      { code: "shiraz", name: "Shiraz" },
      { code: "tabriz", name: "Tabriz" }
    ]
  },
  {
    code: "iraq",
    name: "Iraq",
    states: [
      { code: "baghdad", name: "Baghdad" },
      { code: "basra", name: "Basra" },
      { code: "mosul", name: "Mosul" },
      { code: "erbil", name: "Erbil" },
      { code: "najaf", name: "Najaf" }
    ]
  },
  {
    code: "israel",
    name: "Israel",
    states: [
      { code: "jerusalem", name: "Jerusalem" },
      { code: "tel-aviv", name: "Tel Aviv" },
      { code: "haifa", name: "Haifa" },
      { code: "beersheba", name: "Beersheba" },
      { code: "petah-tikva", name: "Petah Tikva" }
    ]
  },
  {
    code: "jordan",
    name: "Jordan",
    states: [
      { code: "amman", name: "Amman" },
      { code: "zarqa", name: "Zarqa" },
      { code: "irbid", name: "Irbid" },
      { code: "russeifa", name: "Russeifa" }
    ]
  },
  {
    code: "lebanon",
    name: "Lebanon",
    states: [
      { code: "beirut", name: "Beirut" },
      { code: "mount-lebanon", name: "Mount Lebanon" },
      { code: "north-lebanon", name: "North Lebanon" },
      { code: "south-lebanon", name: "South Lebanon" },
      { code: "bekaa", name: "Bekaa" }
    ]
  },
  {
    code: "syria",
    name: "Syria",
    states: [
      { code: "damascus", name: "Damascus" },
      { code: "aleppo", name: "Aleppo" },
      { code: "homs", name: "Homs" },
      { code: "lattakia", name: "Lattakia" }
    ]
  },
  {
    code: "myanmar",
    name: "Myanmar",
    states: [
      { code: "yangon", name: "Yangon" },
      { code: "mandalay", name: "Mandalay" },
      { code: "naypyidaw", name: "Naypyidaw" },
      { code: "bago", name: "Bago" }
    ]
  },
  {
    code: "malaysia",
    name: "Malaysia",
    states: [
      { code: "selangor", name: "Selangor" },
      { code: "johor", name: "Johor" },
      { code: "sabah", name: "Sabah" },
      { code: "sarawak", name: "Sarawak" },
      { code: "perak", name: "Perak" },
      { code: "kedah", name: "Kedah" },
      { code: "pulau-pinang", name: "Pulau Pinang" },
      { code: "kelantan", name: "Kelantan" },
      { code: "pahang", name: "Pahang" },
      { code: "negeri-sembilan", name: "Negeri Sembilan" },
      { code: "melaka", name: "Melaka" },
      { code: "terengganu", name: "Terengganu" },
      { code: "perlis", name: "Perlis" },
      { code: "kuala-lumpur", name: "Kuala Lumpur" },
      { code: "labuan", name: "Labuan" },
      { code: "putrajaya", name: "Putrajaya" }
    ]
  },
  // European Countries
  {
    code: "romania",
    name: "Romania",
    states: [
      { code: "bucharest", name: "Bucharest" },
      { code: "cluj", name: "Cluj" },
      { code: "timis", name: "Timiș" },
      { code: "iasi", name: "Iași" },
      { code: "constanta", name: "Constanța" }
    ]
  },
  {
    code: "bulgaria",
    name: "Bulgaria",
    states: [
      { code: "sofia", name: "Sofia" },
      { code: "plovdiv", name: "Plovdiv" },
      { code: "varna", name: "Varna" },
      { code: "burgas", name: "Burgas" }
    ]
  },
  {
    code: "hungary",
    name: "Hungary",
    states: [
      { code: "budapest", name: "Budapest" },
      { code: "pest", name: "Pest" },
      { code: "bacs-kiskun", name: "Bács-Kiskun" },
      { code: "szabolcs-szatmar-bereg", name: "Szabolcs-Szatmár-Bereg" }
    ]
  },
  {
    code: "czech-republic",
    name: "Czech Republic",
    states: [
      { code: "prague", name: "Prague" },
      { code: "central-bohemia", name: "Central Bohemia" },
      { code: "south-moravia", name: "South Moravia" },
      { code: "moravian-silesia", name: "Moravian-Silesia" }
    ]
  },
  {
    code: "slovakia",
    name: "Slovakia",
    states: [
      { code: "bratislava", name: "Bratislava" },
      { code: "kosice", name: "Košice" },
      { code: "presov", name: "Prešov" },
      { code: "zilina", name: "Žilina" }
    ]
  },
  {
    code: "croatia",
    name: "Croatia",
    states: [
      { code: "zagreb", name: "Zagreb" },
      { code: "split-dalmatia", name: "Split-Dalmatia" },
      { code: "primorje-gorski-kotar", name: "Primorje-Gorski Kotar" },
      { code: "osijek-baranja", name: "Osijek-Baranja" }
    ]
  },
  {
    code: "serbia",
    name: "Serbia",
    states: [
      { code: "belgrade", name: "Belgrade" },
      { code: "novi-sad", name: "Novi Sad" },
      { code: "nis", name: "Niš" },
      { code: "kragujevac", name: "Kragujevac" }
    ]
  },
  {
    code: "bosnia-herzegovina",
    name: "Bosnia and Herzegovina",
    states: [
      { code: "federation-bosnia-herzegovina", name: "Federation of Bosnia and Herzegovina" },
      { code: "republika-srpska", name: "Republika Srpska" },
      { code: "brcko-district", name: "Brčko District" }
    ]
  },
  // Latin American Countries
  {
    code: "colombia",
    name: "Colombia",
    states: [
      { code: "bogota", name: "Bogotá" },
      { code: "antioquia", name: "Antioquia" },
      { code: "valle-del-cauca", name: "Valle del Cauca" },
      { code: "cundinamarca", name: "Cundinamarca" },
      { code: "atlantico", name: "Atlántico" }
    ]
  },
  {
    code: "peru",
    name: "Peru",
    states: [
      { code: "lima", name: "Lima" },
      { code: "la-libertad", name: "La Libertad" },
      { code: "piura", name: "Piura" },
      { code: "cajamarca", name: "Cajamarca" },
      { code: "puno", name: "Puno" }
    ]
  },
  {
    code: "chile",
    name: "Chile",
    states: [
      { code: "santiago", name: "Santiago" },
      { code: "valparaiso", name: "Valparaíso" },
      { code: "bio-bio", name: "Biobío" },
      { code: "araucania", name: "Araucanía" },
      { code: "los-lagos", name: "Los Lagos" }
    ]
  },
  {
    code: "ecuador",
    name: "Ecuador",
    states: [
      { code: "guayas", name: "Guayas" },
      { code: "pichincha", name: "Pichincha" },
      { code: "manabi", name: "Manabí" },
      { code: "los-rios", name: "Los Ríos" },
      { code: "azuay", name: "Azuay" }
    ]
  },
  {
    code: "bolivia",
    name: "Bolivia",
    states: [
      { code: "la-paz", name: "La Paz" },
      { code: "santa-cruz", name: "Santa Cruz" },
      { code: "cochabamba", name: "Cochabamba" },
      { code: "potosi", name: "Potosí" },
      { code: "chuquisaca", name: "Chuquisaca" }
    ]
  },
  {
    code: "uruguay",
    name: "Uruguay",
    states: [
      { code: "montevideo", name: "Montevideo" },
      { code: "canelones", name: "Canelones" },
      { code: "maldonado", name: "Maldonado" },
      { code: "salto", name: "Salto" }
    ]
  },
  {
    code: "paraguay",
    name: "Paraguay",
    states: [
      { code: "asuncion", name: "Asunción" },
      { code: "central", name: "Central" },
      { code: "alto-parana", name: "Alto Paraná" },
      { code: "itapua", name: "Itapúa" }
    ]
  },
  // Additional Important Countries
  {
    code: "south-sudan",
    name: "South Sudan",
    states: [
      { code: "central-equatoria", name: "Central Equatoria" },
      { code: "eastern-equatoria", name: "Eastern Equatoria" },
      { code: "western-equatoria", name: "Western Equatoria" },
      { code: "upper-nile", name: "Upper Nile" }
    ]
  },
  {
    code: "zimbabwe",
    name: "Zimbabwe",
    states: [
      { code: "harare", name: "Harare" },
      { code: "bulawayo", name: "Bulawayo" },
      { code: "manicaland", name: "Manicaland" },
      { code: "mashonaland-central", name: "Mashonaland Central" }
    ]
  },
  {
    code: "zambia",
    name: "Zambia",
    states: [
      { code: "lusaka", name: "Lusaka" },
      { code: "copperbelt", name: "Copperbelt" },
      { code: "southern", name: "Southern" },
      { code: "eastern", name: "Eastern" }
    ]
  },
  {
    code: "madagascar",
    name: "Madagascar",
    states: [
      { code: "antananarivo", name: "Antananarivo" },
      { code: "fianarantsoa", name: "Fianarantsoa" },
      { code: "toamasina", name: "Toamasina" },
      { code: "mahajanga", name: "Mahajanga" }
    ]
  },
  {
    code: "cameroon",
    name: "Cameroon",
    states: [
      { code: "centre", name: "Centre" },
      { code: "littoral", name: "Littoral" },
      { code: "west", name: "West" },
      { code: "northwest", name: "Northwest" },
      { code: "southwest", name: "Southwest" }
    ]
  },
  {
    code: "ivory-coast",
    name: "Ivory Coast",
    states: [
      { code: "abidjan", name: "Abidjan" },
      { code: "yamoussoukro", name: "Yamoussoukro" },
      { code: "bouake", name: "Bouaké" },
      { code: "daloa", name: "Daloa" }
    ]
  },
  {
    code: "senegal",
    name: "Senegal",
    states: [
      { code: "dakar", name: "Dakar" },
      { code: "thies", name: "Thiès" },
      { code: "diourbel", name: "Diourbel" },
      { code: "saint-louis", name: "Saint-Louis" }
    ]
  },
  {
    code: "mali",
    name: "Mali",
    states: [
      { code: "bamako", name: "Bamako" },
      { code: "sikasso", name: "Sikasso" },
      { code: "segou", name: "Ségou" },
      { code: "mopti", name: "Mopti" }
    ]
  },
  {
    code: "burkina-faso",
    name: "Burkina Faso",
    states: [
      { code: "centre", name: "Centre" },
      { code: "hauts-bassins", name: "Hauts-Bassins" },
      { code: "nord", name: "Nord" },
      { code: "centre-ouest", name: "Centre-Ouest" }
    ]
  },
  {
    code: "niger",
    name: "Niger",
    states: [
      { code: "niamey", name: "Niamey" },
      { code: "zinder", name: "Zinder" },
      { code: "maradi", name: "Maradi" },
      { code: "tahoua", name: "Tahoua" }
    ]
  },
  {
    code: "chad",
    name: "Chad",
    states: [
      { code: "ndjamena", name: "N'Djamena" },
      { code: "chari-baguirmi", name: "Chari-Baguirmi" },
      { code: "logone-occidental", name: "Logone Occidental" },
      { code: "mayo-kebbi-est", name: "Mayo-Kebbi Est" }
    ]
  },
  {
    code: "guinea",
    name: "Guinea",
    states: [
      { code: "conakry", name: "Conakry" },
      { code: "kindia", name: "Kindia" },
      { code: "faranah", name: "Faranah" },
      { code: "nzerekore", name: "Nzérékoré" }
    ]
  },
  {
    code: "benin",
    name: "Benin",
    states: [
      { code: "littoral", name: "Littoral" },
      { code: "atlantique", name: "Atlantique" },
      { code: "oueme", name: "Ouémé" },
      { code: "zou", name: "Zou" }
    ]
  },
  {
    code: "togo",
    name: "Togo",
    states: [
      { code: "maritime", name: "Maritime" },
      { code: "plateaux", name: "Plateaux" },
      { code: "centrale", name: "Centrale" },
      { code: "kara", name: "Kara" }
    ]
  },
  {
    code: "liberia",
    name: "Liberia",
    states: [
      { code: "montserrado", name: "Montserrado" },
      { code: "nimba", name: "Nimba" },
      { code: "bong", name: "Bong" },
      { code: "lofa", name: "Lofa" }
    ]
  },
  {
    code: "sierra-leone",
    name: "Sierra Leone",
    states: [
      { code: "western-area", name: "Western Area" },
      { code: "northern", name: "Northern" },
      { code: "southern", name: "Southern" },
      { code: "eastern", name: "Eastern" }
    ]
  },
  // Pacific and Oceanic Countries
  {
    code: "fiji",
    name: "Fiji",
    states: [
      { code: "central", name: "Central" },
      { code: "western", name: "Western" },
      { code: "northern", name: "Northern" },
      { code: "eastern", name: "Eastern" }
    ]
  },
  {
    code: "papua-new-guinea",
    name: "Papua New Guinea",
    states: [
      { code: "national-capital-district", name: "National Capital District" },
      { code: "western-highlands", name: "Western Highlands" },
      { code: "morobe", name: "Morobe" },
      { code: "eastern-highlands", name: "Eastern Highlands" }
    ]
  },
  // Caribbean Countries
  {
    code: "jamaica",
    name: "Jamaica",
    states: [
      { code: "kingston", name: "Kingston" },
      { code: "st-andrew", name: "St. Andrew" },
      { code: "st-catherine", name: "St. Catherine" },
      { code: "clarendon", name: "Clarendon" }
    ]
  },
  {
    code: "haiti",
    name: "Haiti",
    states: [
      { code: "ouest", name: "Ouest" },
      { code: "nord", name: "Nord" },
      { code: "sud", name: "Sud" },
      { code: "artibonite", name: "Artibonite" }
    ]
  },
  {
    code: "dominican-republic",
    name: "Dominican Republic",
    states: [
      { code: "distrito-nacional", name: "Distrito Nacional" },
      { code: "santiago", name: "Santiago" },
      { code: "santo-domingo", name: "Santo Domingo" },
      { code: "la-vega", name: "La Vega" }
    ]
  },
  {
    code: "cuba",
    name: "Cuba",
    states: [
      { code: "havana", name: "Havana" },
      { code: "santiago-de-cuba", name: "Santiago de Cuba" },
      { code: "camaguey", name: "Camagüey" },
      { code: "holguin", name: "Holguín" }
    ]
  },
  // Additional European Countries
  {
    code: "estonia",
    name: "Estonia",
    states: [
      { code: "harju", name: "Harju" },
      { code: "tartu", name: "Tartu" },
      { code: "ida-viru", name: "Ida-Viru" },
      { code: "parnu", name: "Pärnu" }
    ]
  },
  {
    code: "latvia",
    name: "Latvia",
    states: [
      { code: "riga", name: "Riga" },
      { code: "daugavpils", name: "Daugavpils" },
      { code: "liepaja", name: "Liepāja" },
      { code: "jelgava", name: "Jelgava" }
    ]
  },
  {
    code: "lithuania",
    name: "Lithuania",
    states: [
      { code: "vilnius", name: "Vilnius" },
      { code: "kaunas", name: "Kaunas" },
      { code: "klaipeda", name: "Klaipėda" },
      { code: "siauliai", name: "Šiauliai" }
    ]
  },
  {
    code: "slovenia",
    name: "Slovenia",
    states: [
      { code: "central-slovenia", name: "Central Slovenia" },
      { code: "drava", name: "Drava" },
      { code: "savinja", name: "Savinja" },
      { code: "southeast-slovenia", name: "Southeast Slovenia" }
    ]
  },
  {
    code: "north-macedonia",
    name: "North Macedonia",
    states: [
      { code: "skopje", name: "Skopje" },
      { code: "eastern", name: "Eastern" },
      { code: "southwestern", name: "Southwestern" },
      { code: "southeastern", name: "Southeastern" }
    ]
  },
  {
    code: "montenegro",
    name: "Montenegro",
    states: [
      { code: "podgorica", name: "Podgorica" },
      { code: "nikšić", name: "Nikšić" },
      { code: "pljevlja", name: "Pljevlja" },
      { code: "bijelo-polje", name: "Bijelo Polje" }
    ]
  },
  {
    code: "kosovo",
    name: "Kosovo",
    states: [
      { code: "pristina", name: "Pristina" },
      { code: "prizren", name: "Prizren" },
      { code: "peja", name: "Peja" },
      { code: "gjakova", name: "Gjakova" }
    ]
  },
  // Additional Asian Countries
  {
    code: "uzbekistan",
    name: "Uzbekistan",
    states: [
      { code: "tashkent", name: "Tashkent" },
      { code: "samarkand", name: "Samarkand" },
      { code: "bukhara", name: "Bukhara" },
      { code: "fergana", name: "Fergana" }
    ]
  },
  {
    code: "turkmenistan",
    name: "Turkmenistan",
    states: [
      { code: "ashgabat", name: "Ashgabat" },
      { code: "mary", name: "Mary" },
      { code: "turkmenbashi", name: "Turkmenbashi" },
      { code: "dashoguz", name: "Dashoguz" }
    ]
  },
  {
    code: "kyrgyzstan",
    name: "Kyrgyzstan",
    states: [
      { code: "bishkek", name: "Bishkek" },
      { code: "osh", name: "Osh" },
      { code: "jalal-abad", name: "Jalal-Abad" },
      { code: "karakol", name: "Karakol" }
    ]
  },
  {
    code: "tajikistan",
    name: "Tajikistan",
    states: [
      { code: "dushanbe", name: "Dushanbe" },
      { code: "khujand", name: "Khujand" },
      { code: "kulob", name: "Kulob" },
      { code: "qurghonteppa", name: "Qurghonteppa" }
    ]
  },
  {
    code: "armenia",
    name: "Armenia",
    states: [
      { code: "yerevan", name: "Yerevan" },
      { code: "gyumri", name: "Gyumri" },
      { code: "vanadzor", name: "Vanadzor" },
      { code: "vagharshapat", name: "Vagharshapat" }
    ]
  },
  {
    code: "azerbaijan",
    name: "Azerbaijan",
    states: [
      { code: "baku", name: "Baku" },
      { code: "ganja", name: "Ganja" },
      { code: "sumgayit", name: "Sumgayit" },
      { code: "mingachevir", name: "Mingachevir" }
    ]
  },
  {
    code: "georgia",
    name: "Georgia",
    states: [
      { code: "tbilisi", name: "Tbilisi" },
      { code: "kutaisi", name: "Kutaisi" },
      { code: "batumi", name: "Batumi" },
      { code: "rustavi", name: "Rustavi" }
    ]
  },
  // Additional Middle Eastern Countries
  {
    code: "kuwait",
    name: "Kuwait",
    states: [
      { code: "kuwait-city", name: "Kuwait City" },
      { code: "hawalli", name: "Hawalli" },
      { code: "farwaniya", name: "Farwaniya" },
      { code: "mubarak-al-kabeer", name: "Mubarak Al-Kabeer" }
    ]
  },
  {
    code: "qatar",
    name: "Qatar",
    states: [
      { code: "doha", name: "Doha" },
      { code: "al-rayyan", name: "Al Rayyan" },
      { code: "al-wakrah", name: "Al Wakrah" },
      { code: "al-khor", name: "Al Khor" }
    ]
  },
  {
    code: "bahrain",
    name: "Bahrain",
    states: [
      { code: "manama", name: "Manama" },
      { code: "riffa", name: "Riffa" },
      { code: "muharraq", name: "Muharraq" },
      { code: "hamad-town", name: "Hamad Town" }
    ]
  },
  {
    code: "united-arab-emirates",
    name: "United Arab Emirates",
    states: [
      { code: "abu-dhabi", name: "Abu Dhabi" },
      { code: "dubai", name: "Dubai" },
      { code: "sharjah", name: "Sharjah" },
      { code: "ajman", name: "Ajman" },
      { code: "ras-al-khaimah", name: "Ras Al Khaimah" },
      { code: "fujairah", name: "Fujairah" },
      { code: "umm-al-quwain", name: "Umm Al Quwain" }
    ]
  },
  {
    code: "oman",
    name: "Oman",
    states: [
      { code: "muscat", name: "Muscat" },
      { code: "salalah", name: "Salalah" },
      { code: "sohar", name: "Sohar" },
      { code: "nizwa", name: "Nizwa" }
    ]
  },
  {
    code: "yemen",
    name: "Yemen",
    states: [
      { code: "sanaa", name: "Sana'a" },
      { code: "aden", name: "Aden" },
      { code: "taiz", name: "Taiz" },
      { code: "hodeidah", name: "Hodeidah" }
    ]
  },
  // Final Additional Countries
  {
    code: "belarus",
    name: "Belarus",
    states: [
      { code: "minsk", name: "Minsk" },
      { code: "gomel", name: "Gomel" },
      { code: "mogilev", name: "Mogilev" },
      { code: "vitebsk", name: "Vitebsk" }
    ]
  },
  {
    code: "moldova",
    name: "Moldova",
    states: [
      { code: "chisinau", name: "Chișinău" },
      { code: "tiraspol", name: "Tiraspol" },
      { code: "balti", name: "Bălți" },
      { code: "cahul", name: "Cahul" }
    ]
  },
  {
    code: "luxembourg",
    name: "Luxembourg",
    states: [
      { code: "luxembourg-city", name: "Luxembourg City" },
      { code: "esch-sur-alzette", name: "Esch-sur-Alzette" },
      { code: "differdange", name: "Differdange" },
      { code: "dudelange", name: "Dudelange" }
    ]
  },
  {
    code: "malta",
    name: "Malta",
    states: [
      { code: "valletta", name: "Valletta" },
      { code: "birkirkara", name: "Birkirkara" },
      { code: "mosta", name: "Mosta" },
      { code: "qormi", name: "Qormi" }
    ]
  },
  {
    code: "cyprus",
    name: "Cyprus",
    states: [
      { code: "nicosia", name: "Nicosia" },
      { code: "limassol", name: "Limassol" },
      { code: "larnaca", name: "Larnaca" },
      { code: "paphos", name: "Paphos" }
    ]
  },
  {
    code: "iceland",
    name: "Iceland",
    states: [
      { code: "capital-region", name: "Capital Region" },
      { code: "southern-peninsula", name: "Southern Peninsula" },
      { code: "western", name: "Western" },
      { code: "westfjords", name: "Westfjords" }
    ]
  }
];