from vivaldi import types


def format_call(call):

    new_call = types.Call()

    new_call.caller_number = call["caller_number"]
    new_call.audio_identifier = call["call_audio"]
    new_call.created_at = call["created_at"]
    new_call.duration = call["viva_call_duration"]
    new_call.uuid = call["uuid"]

    return new_call


def format_turn(all_turns):
    all_new_turns = []

    for turn in all_turns:
        new_turn = types.Turn()

        # Retaining only turns with turn type specified.

        if "type" in turn.keys():

            new_turn.uuid = turn["uuid"]
            new_turn.type = types.Turn.Type.Value(turn["type"])
            new_turn.sub_type = turn["sub_type"]
            new_turn.state = turn["state"]

            if turn["type"] in ["INPUT"]:
                new_turn.text = turn["user"]

                if turn["sub_type"] in ["AUDIO"]:
                    new_turn.audio_identifier = turn["audio_url"]

                    prediction = eval(
                        turn["prediction"],
                        {},
                        {"false": False, "true": True, "null": None},
                    )
                    metadata = eval(
                        turn["metadata"],
                        {},
                        {"false": False, "true": True, "null": None},
                    )

                    if prediction:

                        for intent in prediction["intents"]:
                            new_intent = types.Intent(
                                name=intent["name"], score=intent["score"]
                            )

                            for slot in intent["slots"]:
                                new_slot = types.Intent.Slot(
                                    name=slot["name"], type=slot["type"][0]
                                )

                                new_intent.slots.append(new_slot)

                            new_turn.prediction.intents.append(new_intent)

                    if metadata:
                        new_turn.language = metadata["language"]
                        new_turn.asr_provider = metadata["asr_provider"]
                        new_turn.audio_identifier = metadata["actual_path"]

            elif turn["type"] in ["RESPONSE"]:
                if turn["sub_type"] in ["TTS"]:
                    new_turn.text = turn["bot"]
                else:
                    # Todo: Add cases where sub-type can be RECORDED, etc.
                    pass
            all_new_turns.append(new_turn)

    return all_new_turns
