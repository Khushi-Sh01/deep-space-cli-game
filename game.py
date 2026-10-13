"""Deep Space Outpost: a short, interactive text adventure."""

import time


TYPE_DELAY = 0.025


def narrate(text):
	"""Print a line with a brief pause for atmosphere."""
	print(text)
	time.sleep(TYPE_DELAY)


def choose(prompt, options):
	"""Ask until the player enters one of the listed option numbers."""
	while True:
		print(prompt)
		for number, option in enumerate(options, start=1):
			print(f"  {number}. {option}")

		answer = input("> ").strip()
		if answer.isdigit() and 1 <= int(answer) <= len(options):
			return int(answer)
		print(f"Please enter a number from 1 to {len(options)}.\n")


def show_status(health, inventory):
	"""Display the astronaut's current condition and carried items."""
	items = ", ".join(inventory) if inventory else "nothing"
	print(f"\n[HEALTH: {health}/3] [INVENTORY: {items}]\n")


def ending(title, text):
	narrate(f"\n=== {title.upper()} ===")
	narrate(text)


def play_game():
	health = 3
	inventory = []

	narrate("DEEP SPACE OUTPOST")
	narrate("You are Dr. Mira Venn, an astrophysicist sent to investigate a signal from")
	narrate("the abandoned orbital station Kestrel-9. Its crew vanished six months ago.")
	narrate("Your shuttle docks with a metallic shudder. Somewhere inside, the signal pulses.")

	choice = choose(
		"At the airlock, what do you do?",
		["Take the emergency med-kit", "Take the portable signal scanner", "Go in empty-handed"],
	)
	if choice == 1:
		inventory.append("med-kit")
		narrate("You secure the med-kit to your suit.")
	elif choice == 2:
		inventory.append("signal scanner")
		narrate("The scanner wakes with a faint, rising whine.")
	else:
		narrate("You leave the supply locker sealed and cycle the airlock.")

	show_status(health, inventory)
	narrate("The station is dark except for a blue pulse seeping beneath the command-deck door.")
	narrate("A maintenance corridor branches left; the command deck lies straight ahead.")

	choice = choose(
		"Where will you investigate first?",
		["Search the maintenance bay", "Head straight to the command deck"],
	)
	if choice == 1:
		narrate("A loose panel snaps shut behind you. You cut your hand on its sharp edge.")
		health -= 1
		if "med-kit" in inventory:
			narrate("You use the med-kit and bind the wound. Your health is restored.")
			health = min(3, health + 1)
			inventory.remove("med-kit")
		else:
			narrate("Without supplies, you wrap the wound in a strip torn from your sleeve.")

		choice = choose(
			"Inside the bay, a tool locker hangs open beside a humming power coupler.",
			["Take the magnetic wrench", "Study the power coupler"],
		)
		if choice == 1:
			inventory.append("magnetic wrench")
			narrate("You take the magnetic wrench. It could force a stubborn hatch.")
		else:
			narrate("The coupler sparks. You pull back before it can burn through your glove.")
			inventory.append("power coupler reading")
	else:
		narrate("The command deck door is jammed. You force it, and a burst of sparks hits your suit.")
		health -= 1
		if "magnetic wrench" in inventory:
			narrate("The wrench absorbs the worst of the impact, but the jolt still rattles you.")

	show_status(health, inventory)
	if health <= 0:
		ending("Lost in the Void", "Your suit fails before you can reach the airlock. Kestrel-9 keeps its silence.")
		return

	narrate("At the command deck, the signal resolves into a voice: 'Mira, do not let them wake it.'")
	narrate("The station's reactor is powering an unknown transmission. A terminal offers two controls:")
	choice = choose(
		"How do you respond?",
		["Analyze the signal before touching anything", "Override the reactor controls"],
	)

	if choice == 1:
		if "signal scanner" in inventory or "power coupler reading" in inventory:
			narrate("Your instruments isolate the signal: it is a distress beacon, looped by a hidden relay.")
			narrate("The relay's maintenance key is tucked behind the terminal. You can shut it down safely.")
			choice = choose(
				"What do you do with the discovery?",
				["Disable the relay and transmit the crew's coordinates", "Leave the relay running and follow the beacon"],
			)
			if choice == 1:
				ending("Success", "The beacon cuts out. A rescue ship answers your transmission, and Kestrel-9 is finally quiet.")
			else:
				ending("Lost in the Void", "The beacon leads you beyond the station. Your shuttle never receives another signal.")
		else:
			narrate("Without an instrument, the shifting waveform is impossible to decode. The relay begins to overload.")
			choice = choose(
				"You have seconds to act.",
				["Pull the relay's power cable", "Seal the command deck and retreat"],
			)
			if choice == 1:
				ending("Sabotaged", "The cable is already cut. The reactor surges, and someone has rigged the outpost to fail.")
			else:
				ending("Lost in the Void", "The blast throws you into the dark between the station and your shuttle.")
	else:
		if "magnetic wrench" in inventory:
			narrate("The wrench cracks open the control housing. You spot a tampered relay before the override completes.")
			choice = choose(
				"The relay is wired to the reactor. Choose quickly.",
				["Disconnect the relay", "Force the override anyway"],
			)
			if choice == 1:
				ending("Success", "The false transmission dies. You secure the station and send a clear report home.")
			else:
				ending("Sabotaged", "The relay was booby-trapped. The override triggers the station's failsafe.")
		else:
			narrate("The controls reject your command. A hidden failsafe locks the doors and vents the deck.")
			ending("Sabotaged", "Someone altered the reactor before the crew disappeared. The station seals around you.")

	print("\nThanks for playing Deep Space Outpost.")


if __name__ == "__main__":
	play_game()
