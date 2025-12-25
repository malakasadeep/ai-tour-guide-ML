import pandas as pd
import numpy as np
import random

# ==========================================
# 1. THE KNOWLEDGE BASE (75 Locations with REAL Coordinates)
# ==========================================
# Format: [History, Adventure, Nature, Relax, Outdoor(0/1), Lat, Lng]
LOCATION_DB = {
    # --- SIGIRIYA / DAMBULLA HUB ---
    "Sigiriya Lion Rock": [1.0, 0.4, 0.5, 0.1, 1, 7.9570, 80.7603],
    "Pidurangala Rock": [0.6, 0.8, 0.6, 0.2, 1, 7.9636, 80.7633],
    "Dambulla Cave Temple": [1.0, 0.2, 0.3, 0.3, 0, 7.8565, 80.6484],
    "Minneriya National Park": [0.1, 0.6, 1.0, 0.2, 1, 8.0305, 80.8306],
    "Ritigala Forest Monastery": [0.9, 0.5, 0.8, 0.2, 1, 8.1189, 80.6483],
    "Hiriwadunna Village Trek": [0.3, 0.2, 0.7, 0.8, 1, 8.0197, 80.7631],
    "Rose Quartz Mountain": [0.4, 0.6, 0.8, 0.2, 1, 7.8400, 80.5600],

    # --- KANDY HUB ---
    "Temple of the Tooth": [1.0, 0.1, 0.2, 0.6, 0, 7.2936, 80.6413],
    "Royal Botanical Gardens": [0.3, 0.1, 0.9, 0.8, 1, 7.2697, 80.5967],
    "Udawattekele Sanctuary": [0.2, 0.5, 0.9, 0.4, 1, 7.2989, 80.6433],
    "Bahirawakanda Buddha": [0.7, 0.2, 0.3, 0.5, 1, 7.2913, 80.6300],
    "Ceylon Tea Museum": [0.8, 0.0, 0.2, 0.6, 0, 7.2683, 80.6319],
    "Ambuluwawa Tower": [0.2, 0.7, 0.6, 0.2, 1, 7.1614, 80.5562],
    "Hanthana Mountain Range": [0.1, 0.8, 0.8, 0.1, 1, 7.2586, 80.6286],
    "Kandy Lake Stroll": [0.4, 0.1, 0.5, 0.9, 1, 7.2925, 80.6410],
    "Embekke Devalaya": [1.0, 0.1, 0.2, 0.4, 0, 7.2186, 80.5658],

    # --- NUWARA ELIYA HUB ---
    "Gregory Lake": [0.1, 0.2, 0.6, 0.8, 1, 6.9583, 80.7764],
    "Horton Plains": [0.1, 0.8, 1.0, 0.2, 1, 6.8028, 80.8039],
    "Pedro Tea Estate": [0.4, 0.1, 0.6, 0.8, 1, 6.9833, 80.7833],
    "Moon Plains": [0.1, 0.5, 0.9, 0.4, 1, 6.9583, 80.8000],
    "Hakgala Botanical Garden": [0.2, 0.1, 0.9, 0.7, 1, 6.9274, 80.8201],
    "Victoria Park": [0.3, 0.0, 0.8, 0.8, 1, 6.9708, 80.7675],
    "Strawberry Farm Visit": [0.0, 0.0, 0.6, 0.9, 0, 6.9400, 80.7400],
    "St. Clair's Falls": [0.1, 0.3, 0.9, 0.6, 1, 6.9389, 80.6464],

    # --- ELLA HUB ---
    "Ella Rock Hike": [0.1, 0.9, 0.8, 0.1, 1, 6.8585, 81.0505],
    "Nine Arches Bridge": [0.6, 0.3, 0.7, 0.4, 1, 6.8768, 81.0608],
    "Little Adam's Peak": [0.1, 0.8, 0.8, 0.2, 1, 6.8667, 81.0667],
    "Ravana Falls": [0.2, 0.3, 0.8, 0.5, 1, 6.8417, 81.0500],
    "Lipton's Seat": [0.3, 0.5, 0.9, 0.4, 1, 6.7833, 81.0167],
    "Diyaluma Falls": [0.1, 0.9, 0.9, 0.3, 1, 6.7303, 81.0319],
    "Adisham Bungalow": [0.8, 0.1, 0.4, 0.6, 0, 6.7767, 80.9250],

    # --- GALLE / SOUTH ---
    "Galle Fort": [0.9, 0.1, 0.2, 0.8, 1, 6.0311, 80.2170],
    "Unawatuna Jungle Beach": [0.1, 0.5, 0.7, 0.8, 1, 6.0183, 80.2525],
    "Japanese Peace Pagoda": [0.7, 0.1, 0.4, 0.8, 1, 6.0150, 80.2433],
    "Koggala Lake Safari": [0.1, 0.2, 0.8, 0.8, 1, 5.9833, 80.3167],
    "Sea Turtle Hatchery": [0.1, 0.1, 0.7, 0.5, 0, 5.9833, 80.2833],
    "Mirissa Whale Watching": [0.0, 0.8, 0.9, 0.3, 1, 5.9483, 80.4714],
    "Coconut Tree Hill": [0.0, 0.1, 0.5, 0.9, 1, 5.9381, 80.4667],
    "Weligama Surf Break": [0.0, 0.9, 0.4, 0.3, 1, 5.9667, 80.4333],
    "Hikkaduwa Coral Reef": [0.1, 0.6, 0.7, 0.5, 1, 6.1389, 80.1000],
    "Madol Doova": [0.4, 0.2, 0.7, 0.5, 1, 5.9667, 80.3000],

    # --- ANCIENT CITIES ---
    "Anuradhapura Sacred City": [1.0, 0.1, 0.3, 0.2, 1, 8.3500, 80.3949],
    "Mihintale": [1.0, 0.3, 0.4, 0.2, 1, 8.3500, 80.5167],
    "Polonnaruwa Ruins": [1.0, 0.2, 0.4, 0.2, 1, 7.9333, 81.0000],
    "Parakrama Samudra": [0.4, 0.1, 0.6, 0.8, 1, 7.9333, 81.0000],
    "Wilpattu National Park": [0.2, 0.6, 1.0, 0.2, 1, 8.4333, 80.0000],
    "Yapahuwa Rock Fortress": [0.9, 0.4, 0.4, 0.1, 1, 7.8168, 80.3107],
    "Avukana Buddha Statue": [0.9, 0.1, 0.2, 0.5, 1, 8.0100, 80.5100],

    # --- EAST COAST ---
    "Trincomalee Harbour": [0.5, 0.2, 0.6, 0.4, 1, 8.5667, 81.2333],
    "Koneswaram Temple": [0.9, 0.1, 0.5, 0.4, 1, 8.5825, 81.2456],
    "Nilaveli Beach": [0.1, 0.2, 0.5, 0.9, 1, 8.6833, 81.2000],
    "Pigeon Island": [0.1, 0.7, 0.9, 0.3, 1, 8.7167, 81.2000],
    "Marble Beach": [0.1, 0.2, 0.6, 0.9, 1, 8.5167, 81.2167],
    "Pasikudah Beach": [0.1, 0.1, 0.5, 1.0, 1, 7.9167, 81.5500],
    "Arugam Bay": [0.1, 0.9, 0.6, 0.4, 1, 6.8417, 81.8333],
    "Kumana Bird Sanctuary": [0.1, 0.4, 1.0, 0.4, 1, 6.5131, 81.6878],
    "Elephant Rock": [0.0, 0.6, 0.7, 0.5, 1, 6.8100, 81.8200],

    # --- COLOMBO & WEST ---
    "Gangaramaya Temple": [0.8, 0.0, 0.1, 0.5, 0, 6.9169, 79.8550],
    "Lotus Tower": [0.1, 0.3, 0.1, 0.7, 0, 6.9269, 79.8583],
    "Independence Square": [0.7, 0.0, 0.2, 0.6, 1, 6.9039, 79.8678],
    "Galle Face Green": [0.3, 0.1, 0.1, 0.8, 1, 6.9269, 79.8433],
    "Old Dutch Hospital": [0.7, 0.1, 0.1, 0.9, 0, 6.9333, 79.8417],
    "Mount Lavinia Beach": [0.2, 0.1, 0.4, 0.8, 1, 6.8333, 79.8667],
    "Kelaniya Raja Maha Vihara": [0.9, 0.0, 0.1, 0.5, 0, 6.9500, 79.9167],
    "Negombo Fish Market": [0.3, 0.1, 0.2, 0.2, 1, 7.2000, 79.8333],
    "Muthurajawela Wetland": [0.1, 0.4, 0.9, 0.4, 1, 7.0333, 79.8500],

    # --- NORTH (JAFFNA) ---
    "Jaffna Public Library": [0.8, 0.0, 0.1, 0.5, 0, 9.6611, 80.0111],
    "Nallur Kandaswamy Kovil": [0.9, 0.0, 0.0, 0.6, 0, 9.6745, 80.0293],
    "Jaffna Fort": [0.9, 0.2, 0.3, 0.4, 1, 9.6611, 80.0083],
    "Delft Island": [0.7, 0.5, 0.7, 0.2, 1, 9.5100, 79.6800],
    "Nagadeepa Vihara": [0.8, 0.1, 0.4, 0.4, 1, 9.6167, 79.7667],
    "Casuarina Beach": [0.1, 0.2, 0.5, 0.8, 1, 9.7600, 79.8900],
    "Point Pedro": [0.4, 0.3, 0.5, 0.3, 1, 9.8167, 80.2333],

    # --- OTHER NATURE ---
    "Yala National Park": [0.1, 0.7, 1.0, 0.2, 1, 6.3667, 81.4667],
    "Udawalawe National Park": [0.1, 0.6, 1.0, 0.2, 1, 6.4333, 80.8833],
    "Sinharaja Forest Reserve": [0.1, 0.7, 1.0, 0.2, 1, 6.4167, 80.5000],
    "Kitulgala Rafting": [0.1, 1.0, 0.7, 0.1, 1, 6.9833, 80.4167],
    "Bambarakanda Falls": [0.1, 0.7, 0.9, 0.3, 1, 6.7700, 80.8300],
    "Riverston Gap": [0.1, 0.8, 0.9, 0.1, 1, 7.5167, 80.7333],
    "Sembuwatta Lake": [0.1, 0.3, 0.8, 0.7, 1, 7.4369, 80.6997]
}

# ==========================================
# 2. THE META-LEARNING ARCHETYPES
# ==========================================
ARCHETYPES = {
    "Backpacker":  [0.2, 0.9, 0.7, 0.3],
    "Historian":   [0.9, 0.2, 0.4, 0.4],
    "Luxury_Relax": [0.1, 0.1, 0.4, 0.9],
    "Nature_Lover": [0.2, 0.6, 0.9, 0.5],
    "Family_Vacation": [0.4, 0.3, 0.5, 0.7],
    "Digital_Nomad": [0.1, 0.5, 0.5, 0.8]
}

def generate_synthetic_data(num_users=600, interactions_per_user=15):
    data_rows = []
    
    # 1. Loop through Users
    for user_id in range(1, num_users + 1):
        arch_name = random.choice(list(ARCHETYPES.keys()))
        base_prefs = ARCHETYPES[arch_name]
        
        # Add Noise to User Profile
        u_hist = np.clip(base_prefs[0] + np.random.normal(0, 0.1), 0, 1)
        u_adv  = np.clip(base_prefs[1] + np.random.normal(0, 0.1), 0, 1)
        u_nat  = np.clip(base_prefs[2] + np.random.normal(0, 0.1), 0, 1)
        u_rel  = np.clip(base_prefs[3] + np.random.normal(0, 0.1), 0, 1)
        
        # 2. Simulate Visits
        visited_locs = random.sample(list(LOCATION_DB.keys()), interactions_per_user)
        
        for loc_name in visited_locs:
            l_stats = LOCATION_DB[loc_name]
            # UNPACK ALL 7 VALUES (removed price)
            l_hist, l_adv, l_nat, l_rel, l_outdoor, l_lat, l_lng = l_stats
            
            is_raining = 1 if random.random() < 0.2 else 0 
            
            # --- SPECIALIST BOOST SCORING ALGORITHM ---
            # Calculate individual matches for each interest category
            match_hist = u_hist * l_hist
            match_adv = u_adv * l_adv
            match_nat = u_nat * l_nat
            match_rel = u_rel * l_rel
            
            # Identify the primary hook (strongest match)
            all_matches = [match_hist, match_adv, match_nat, match_rel]
            primary_match = max(all_matches)
            
            # Calculate average of the other three matches
            other_matches = [m for m in all_matches if m != primary_match]
            avg_others = sum(other_matches) / len(other_matches) if other_matches else 0.0
            
            # Weighted formula: Primary interest drives 70% of the decision
            base_score = (primary_match * 7.0) + (avg_others * 3.0)
            
            # Passion bonus: Reward strong alignment in primary interest
            passion_bonus = 0.0
            if primary_match > 0.8:
                passion_bonus = 1.5
            
            # Weather penalty: Stronger penalty for outdoor activities in rain
            weather_penalty = 0.0
            if is_raining == 1 and l_outdoor == 1:
                weather_penalty = 5.0
            
            # Calculate final score with noise
            final_score = base_score + passion_bonus - weather_penalty
            final_score += np.random.uniform(-0.5, 0.5)  # Small random noise
            final_score = np.clip(final_score, 0.0, 10.0)
            
            row = {
                "User_ID": f"U{user_id:04d}",
                "User_Archetype": arch_name,
                "u_hist": round(u_hist, 2),
                "u_adv": round(u_adv, 2),
                "u_nat": round(u_nat, 2),
                "u_rel": round(u_rel, 2),
                "Location_Name": loc_name,
                "l_hist": l_hist,
                "l_adv": l_adv,
                "l_nat": l_nat,
                "l_rel": l_rel,
                "l_outdoor": l_outdoor,
                "l_lat": l_lat,
                "l_lng": l_lng,
                "c_raining": is_raining,
                "ENJOYMENT_SCORE": round(final_score, 1)
            }
            data_rows.append(row)
            
    return pd.DataFrame(data_rows)

if __name__ == "__main__":
    print(f"Generating Data for {len(LOCATION_DB)} Locations...")
    df = generate_synthetic_data(num_users=600, interactions_per_user=15)
    
    # Save files
    df.to_csv("training_interactions.csv", index=False)
    
    # Save Metadata with Lat/Lng
    loc_cols = ['Location_Name', 'l_hist', 'l_adv', 'l_nat', 'l_rel', 'l_outdoor', 'l_lat', 'l_lng']
    loc_metadata = df[loc_cols].drop_duplicates()
    loc_metadata.to_csv("locations_metadata.csv", index=False)
    
    print(f"✅ Success! Generated {len(df)} rows. Includes accurate GPS coordinates.")