import csv
import os
import cv2
import numpy as np
import pandas as pd
import datetime
import time


def TakeImage(
    l1,
    l2,
    haarcasecade_path,
    trainimage_path,
    message,
    err_screen,
    text_to_speech,
):

    if (l1 == "") and (l2 == ""):
        text_to_speech(
            "Please Enter your Enrollment Number and Name."
        )
        return

    elif l1 == "":
        text_to_speech(
            "Please Enter your Enrollment Number."
        )
        return

    elif l2 == "":
        text_to_speech(
            "Please Enter your Name."
        )
        return

    try:

        cam = cv2.VideoCapture(0)

        detector = cv2.CascadeClassifier(
            haarcasecade_path
        )

        Enrollment = str(l1).strip()
        Name = str(l2).strip()

        sampleNum = 0

        directory = f"{Enrollment}_{Name}"

        path = os.path.join(
            trainimage_path,
            directory
        )

        os.makedirs(path, exist_ok=False)

        while True:

            ret, img = cam.read()

            if not ret:
                break

            gray = cv2.cvtColor(
                img,
                cv2.COLOR_BGR2GRAY
            )

            faces = detector.detectMultiScale(
                gray,
                1.3,
                5
            )

            for (x, y, w, h) in faces:

                cv2.rectangle(
                    img,
                    (x, y),
                    (x + w, y + h),
                    (255, 0, 0),
                    2
                )

                sampleNum += 1

                image_path = os.path.join(
                    path,
                    f"{Name}_{Enrollment}_{sampleNum}.jpg"
                )

                cv2.imwrite(
                    image_path,
                    gray[y:y + h, x:x + w]
                )

                cv2.imshow(
                    "Frame",
                    img
                )

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

            elif sampleNum >= 50:
                break

        cam.release()
        cv2.destroyAllWindows()

        # ------------------------------------------------
        # Save student details
        # ------------------------------------------------

        BASE_DIR = os.path.dirname(
            os.path.abspath(__file__)
        )

        student_csv = os.path.join(
            BASE_DIR,
            "StudentDetails",
            "studentdetails.csv"
        )

        os.makedirs(
            os.path.dirname(student_csv),
            exist_ok=True
        )

        row = [Enrollment, Name]

        with open(
            student_csv,
            "a+",
            newline=""
        ) as csvFile:

            writer = csv.writer(
                csvFile,
                delimiter=","
            )

            writer.writerow(row)

        res = (
            f"Images Saved for ER No: "
            f"{Enrollment} Name: {Name}"
        )

        message.configure(text=res)

        text_to_speech(res)

    except FileExistsError:

        msg = "Student Data already exists"

        message.configure(text=msg)

        text_to_speech(msg)

    except Exception as e:

        print("Error:", e)

        text_to_speech(
            "Error while capturing images."
        )