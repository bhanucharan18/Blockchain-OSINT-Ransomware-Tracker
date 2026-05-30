SIMULATED_TRAIL = {
    "Victim_Wallet": [("Ransom_Address_1A", 5.0)],

    "Ransom_Address_1A": [
        ("Intermediate_Wallet_2B", 4.95),
        ("Fee_Address_01", 0.05)
    ],

    "Intermediate_Wallet_2B": [
        ("Aggregator_Wallet_3C", 4.0),
        ("Change_Address_2C", 0.95)
    ],

    "Aggregator_Wallet_3C": [
        ("Split_A_4D", 5.0),
        ("Split_B_4E", 5.0)
    ],

    "Split_A_4D": [("Mixer_Entry_5F", 5.0)],
    "Split_B_4E": [("Mixer_Entry_5F", 5.0)],

    "Mixer_Entry_5F": [
        ("Attacker_Cold_Storage_FINAL", 9.8)
    ]
}
