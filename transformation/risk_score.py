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