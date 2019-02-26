from battlefield import Battlefield


def main():
    battlefield = Battlefield()
    instructions = battlefield.load_file_instructions()
    battlefield.execute_instructions(instructions)
    battlefield.save_output()


if __name__ == "__main__":
    main()
