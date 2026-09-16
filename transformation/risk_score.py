class RiskCalculator:
    
    


        
    def calculate_score(self, data):

            data = data.copy()

            data["temperature_risk"] = data["temperature_max"].apply(
                lambda temperature:
                    75 if temperature < 5
                    else 25 if temperature < 15
                    else 0 if temperature < 30
                    else 50 if temperature < 40
                    else 100
            )

            data["precipitation_risk"] = data["precipitation_sum"].apply(
                lambda precipitation:
                    0 if precipitation == 0
                    else 20 if precipitation < 5
                    else 50 if precipitation < 20
                    else 75 if precipitation < 50
                    else 100
            )

            data["wind_risk"] = data["wind_speed_10m_max"].apply(
                lambda wind_speed: 
                    0 if wind_speed < 20
                    else 30 if wind_speed < 40
                    else 70 if wind_speed < 60
                    else 100
            )

            data["risk_score"] = (
                data["temperature_risk"] * 0.25
                + data["precipitation_risk"] * 0.40
                + data["wind_risk"] * 0.35
            )

            data["risk_score"] = data["risk_score"].round(2)
            
            data["risk_level"] = data["risk_score"].apply(
                lambda score: 
                    "low" if score < 25
                    else "Moderate" if score < 50
                    else "High" if score < 75
                    else "Critical"
                    
            )

            return data
        
    