"""Offline notification hysteresis prototype; does not qualify bearing condition."""
import math


class StableEpisodes:
    def __init__(self, enter=1.5, clear=1.2, enter_count=3, clear_count=5, max_gap=900):
        if not 0 < clear < enter or enter_count < 1 or clear_count < 1 or max_gap <= 0:
            raise ValueError("Invalid hysteresis policy")
        self.enter, self.clear = enter, clear
        self.enter_count, self.clear_count, self.max_gap = enter_count, clear_count, max_gap
        self.previous = None
        self.streak = [0, 0]
        self.clear_streak = 0
        self.active = False

    def update(self, timestamp, ratios, eligible=True):
        if not math.isfinite(timestamp) or len(ratios) != 2 or any(not math.isfinite(v) or v < 0 for v in ratios):
            raise ValueError("Invalid observation")
        if self.previous is not None and timestamp <= self.previous:
            raise ValueError("Observations must be strictly ordered")
        interrupted = self.previous is not None and timestamp-self.previous > self.max_gap
        self.previous = timestamp
        if interrupted or not eligible:
            self.active = False
            self.streak = [0, 0]
            self.clear_streak = 0
        if not eligible:
            return {"opened": False, "cleared": False, "active": False, "interrupted": True}
        for c in (0, 1):
            self.streak[c] = self.streak[c]+1 if ratios[c] > self.enter else 0
        opened = not self.active and max(self.streak) >= self.enter_count
        if opened:
            self.active = True
        cleared = False
        if self.active:
            self.clear_streak = self.clear_streak+1 if all(v <= self.clear for v in ratios) else 0
            if self.clear_streak >= self.clear_count:
                self.active = False
                self.clear_streak = 0
                self.streak = [0, 0]
                cleared = True
        return {"opened": opened, "cleared": cleared, "active": self.active,
                "interrupted": interrupted}
