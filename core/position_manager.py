class PositionManager:
    def check_exposure(self):
        """实时风险暴露检查"""
        for exchange in self.active_positions:
            net_exposure = sum(pos['notional'] for pos in exchange.positions)
            if net_exposure > self.max_allowed_exposure:
                self.trigger_risk_control()

    def trigger_risk_control(self):
        """自动风控措施"""
        self.logger.critical("触发风险控制机制！")
        self.emergency_close_all()