from knight_fight import KnightFight


def main():
    fight = KnightFight()
    instructions = fight.load_file_instructions()
    fight.execute_instructions(instructions)
    fight.save_output()


if __name__ == "__main__":
    main()
