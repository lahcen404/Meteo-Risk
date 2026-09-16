class RiskCalculator:
    
    

    def temperature_risk(self, temperature):

        if temperature < 5:
            return 75

        elif temperature < 15:
            return 25

        elif temperature < 30:
            return 0

        elif temperature < 40:
            return 50

        else:
            return 100
        
    def precipitation_risk(self, precipitation):

        if precipitation == 0:
            return 0

        elif precipitation < 5:
            return 20

        elif precipitation < 20:
            return 50

        elif precipitation < 50:
            return 75

        else:
            return 100
        
    def wind_risk(self, wind_speed):

        if wind_speed < 20:
            return 0

        elif wind_speed < 40:
            return 30

        elif wind_speed < 60:
            return 70

        else:
            return 100
        
        
    def calculate_score(self, data):

            data = data.copy()

            data["temperature_risk"] = data["temperature_max"].apply(
                self.temperature_risk
            )

            data["precipitation_risk"] = data["precipitation_sum"].apply(
                self.precipitation_risk
            )

            data["wind_risk"] = data["wind_speed_10m_max"].apply(
                self.wind_risk
            )

            data["risk_score"] = (
                data["temperature_risk"] * 0.25
                + data["precipitation_risk"] * 0.40
                + data["wind_risk"] * 0.35
            )

            data["risk_score"] = data["risk_score"].round(2)

            return data