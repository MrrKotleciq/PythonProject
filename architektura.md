mermaid
graph TD
    %% Entry Points
    subgraph Entry_Points [Punkty Wejścia]
        main.py((main.py))
        test.py((test.py))
    end

    %% Core Logic (Classes)
    subgraph Core_OOP [Logika Biznesowa - OOP]
        DM[classes/data_manager.py<br/>DataManager]
        IL[classes/indicators.py<br/>IndicatorLibrary]
        SB[classes/strategy_base.py<br/>StrategyBase]
        STR[classes/strategies.py<br/>SMA & Trend Strategies]
        PA[classes/analyzer.py<br/>PerformanceAnalyzer]
        VZ[classes/visualizer.py<br/>Visualizer]
    end

    %% Utilities
    subgraph Utils [Narzędzia]
        MF[my_fun.py<br/>Helper Functions]
    end

    %% Legacy Code
    subgraph Legacy [Kod Dziedziczny - Proceduralny]
        OM[old_fun/old_main.py]
        OBT[old_fun/old_back_test.py]
        OMF[old_fun/old_my_fun.py]
        OGP[old_fun/old_get_param_script.py]
    end

    %% Relationships
    main.py --> DM
    main.py --> IL
    main.py --> STR
    main.py --> PA
    main.py --> VZ
    main.py --> MF
    
    test.py --> DM
    test.py --> IL
    test.py --> STR
    test.py --> PA
    test.py --> VZ
    test.py --> MF

    STR --> SB
    
    OM --> OBT
    OGP --> OBT
    OBT --> OMF

    %% Styling
    style main.py fill:#f9f,stroke:#333,stroke-width:4px
    style test.py fill:#f9f,stroke:#333,stroke-width:4px
    style Core_OOP fill:#e1f5fe,stroke:#01579b
    style Legacy fill:#ffebee,stroke:#c62828,stroke-dasharray: 5 5
    style Utils fill:#fff3e0,stroke:#ef6c00