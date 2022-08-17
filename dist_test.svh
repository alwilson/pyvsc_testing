class test_class;
    rand logic[31:0] num0;
    rand logic[31:0] num1;

    // Triangle with hole
    constraint nums_c {
        num0 >= 0;
        num1 >= 0;
        num0 <= 60;
        num1 <= 60;
        // !(num0 >= 5 && num0 <= 10 && num1 >= 5 && num1 <= 10);
        // num0 < 5 || num0 > 10 || num1 < 5 || num1 > 10;
        num0 + num1 <= 50;
    };

    // Quarter circle
    // constraint nums_c {
    //    num0 >= 0;
    //    num1 >= 0;
    //    num0 <= 60;
    //    num1 <= 60;
    //    num0*num0 + num1*num1 <= 50*50;
    // };
endclass

module top;

    reg clk;

    initial begin
        int success;
        int fd;
        test_class test0;

        fd = $fopen("./plot.csv", "w");
        test0 = new();

        $system("date +%s.%N");
        for (int i = 0; i < 100000; i++) begin
            success = test0.randomize();
            if(!success)
                $display("randomize failed");
            $fdisplay(fd, "%0d,%0d", test0.num0, test0.num1);
        end
        $system("date +%s.%N");

        $fclose(fd);
    end
endmodule

