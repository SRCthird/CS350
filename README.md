# CS350

## **Summarize the project and what problem it was solving.**  
This project is a smart thermostat prototype using a Raspberry Pi, sensors, buttons, an LCD, and LEDs. It pretends to control heating and cooling based on temperature, cycles through states, and provides visual feedback. It simulates a real thermostat's behavior with status updates via serial communication.
  - MyDisplay.py is a display of information about current datetime, humidity and temp with user inputs only to scroll through screens, pause, and resume.
  - Thermostate.py is a moch backend to the thermostate, checking the current temp and allowing the user to modify the set temp, and whether it is heating or cooling.
  - ThermostateServer-Simulation.py is a moch database for the information recieved through UAT of Thermostate.py.

## **What did you do particularly well?**  
For Thermostate.py I implemented a structured **state machine** for clear and scalable logic. **Multithreading** kept the UI responsive while handling background tasks. Debugging messages provided useful tracking of state transitions. Lastly, for MyDisplay.py I chose to try and create my own **state machine** instead of using a prebuilt library.

## **Where could you improve?**  
I probably could use better **error handling** for sensor failures and communication issues. I'm really running under the assumption that the sensors are just going to work, but thats not always the case. Optimizing **power consumption** by reducing unnecessary LCD and LED updates would help. Using **async programming** instead of threads could improve efficiency.

## **What tools and/or resources are you adding to your support network?**  
I'm planning on adding wifi enabled websocketeting insread of UAT for data logging, as UAT requires a physical connection, while `ws` can allow for web connections that broadcast the data. Of course this will probably have to be `wss` for encryption and something like an API key for security.

## **What skills from this project will be particularly transferable?**  
I learned a lot about **state machine design**, **multithreading**, and **hardware-software integration**. Debugging and testing for embedded systems are now more structured. These skills apply to IoT, automation, and real-time systems.

## **How did you make this project maintainable, readable, and adaptable?**  
I used **clear documentation**, **modular design**, and a **class-based approach**. The `DEBUG` flag simplifies troubleshooting, and **structured serial output** ensures future compatibility. This design makes extensions, like IoT connectivity, easy.
