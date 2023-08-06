# Some codes:
-

# Some databases
- http://nucleardata.nuclear.lu.se/toi/nuclide.asp?iZA=260059
- https://www.nndc.bnl.gov/nudat2/indx_dec.jsp

# Project: nuphy2

## Module: react




|            | In    | FireWrks   | Fully |        | In     |                          |                    |
| module     | Place | ParamCheck | Func  | Pytest | BinDir | description1             | description2       |
|------------+-------+------------+-------+--------+--------+--------------------------+--------------------|
| prj_utils  | y     | NO         | NEVER | NO     | NO     | Color,Fail,Print,GetFile |                    |
| isotope    | y     | y          | ~     | y      | y      | gives isotope data       | used by kinematics |
| kinematics | y     | y          | y     | y      | y      | kinematic calc           |                    |
| rolfs      | y     | y          | y     | y      |        |                          |                    |
| srim       | y     |            |       |        |        |                          |                    |
| xsections  |       |            |       |        |        |                          |                    |
| yields     |       |            |       |        |        |                          |                    |
| radcap     |       |            |       |        |        |                          |                    |
| tendl      |       |            |       |        |        |                          |                    |
|------------+-------+------------+-------+--------+--------+--------------------------+--------------------|
| fispact    |       |            |       |        |        | from nuphy1              |                    |
| sr         |       |            |       |        |        | nuphy1                   |                    |
| spectra    |       |            |       |        |        | nuphy1                   |                    |
./srim.py -i h1 -m al -e 24.4 -t 3mm -n 300 -w a.h5
