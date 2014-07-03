program extract
    implicit none
      real :: lat, long, depth, mag 
      integer :: year
      character(len=*),parameter :: fmt_in = "(12x,i4,1x,f6.1,1x,f8.3,1x,f7.1,2x,f4.1)"
      character(len=*),parameter :: fmt_out = "(i4,2x,f7.2,2x,f7.2,2x,f5.1,2x,f3.1)"

        do while (.true.)
          read (*,fmt_in, end=17) year, lat, long, depth, mag
          write(*,fmt_out, err=17) year,lat,long,depth,mag
        end do

 17 continue

 end program
              
