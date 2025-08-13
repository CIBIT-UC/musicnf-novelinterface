def calc_signal_var(baseline, value, maxPSC):
    """
    Calculates NF Signal.

    Args:
        baseline: float - baseline value for current time point
        value: float - BOLD value at current time point
        maxPSC: float - maximum variation (percent value)

    Returns:
        float: Normalized signal variance
    """
    signal_var = (value - baseline) * 100 / baseline
    signal_var_norm = signal_var / maxPSC
    signal_var_final = min(max(signal_var_norm, 0), 1)

    return signal_var_final