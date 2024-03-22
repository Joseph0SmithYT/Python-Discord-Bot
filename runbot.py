import main
import sys



if len(sys.argv) == 1:
    main.start_bot("QUORTLE")
else:
    main.start_bot(sys.argv[1].upper())