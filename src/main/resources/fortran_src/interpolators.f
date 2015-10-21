      subroutine linint2index(x,xtab,y,dtab)
      implicit none
C     returns the broken index of a 1-d table
C     in python notation (zero indexed)
c     automatic clipping
CF2PY INTENT(IN) :: x,xtab
CF2PY INTENT(OUT) :: y
CF2PY INTENT(HIDE) :: dtab
CF2PY DOUBLE :: xtab(dtab)
CF2PY DOUBLE :: x,y
CF2PY INTEGER :: dtab
      INTEGER j
      INTEGER  dtab
      DOUBLE PRECISION x,xtab(dtab),y
      
        if (x .le. xtab(1)) then 
          y = 0.d0
        else if (x .ge. xtab(dtab)) then 
          y = dble(dtab) -1.d0
        else   
            do j = 2, dtab-1
                if (x .lt. xtab(j)) exit
            enddo   
            y=dble(j-1)+(x-xtab(j-1))/(xtab(j)-xtab(j-1))-1.d0
        endif
      end

      
      subroutine linint2index_vector(x,xtab,y,din,dtab)
      implicit none
C     returns the broken index of a 1-d table
C     in python notation (zero indexed)
c     automatic clipping
CF2PY INTENT(IN) :: x,xtab
CF2PY INTENT(OUT) :: y
CF2PY INTENT(HIDE) :: dtab
CF2PY DOUBLE :: xtab(dtab)
CF2PY DOUBLE :: x(din),y(din)
      INTEGER i
      INTEGER din, dtab
      DOUBLE PRECISION x(din),xtab(dtab),y(din)      
      do i = 1, din
        call linint2index(x(i),xtab,y(i),dtab)
      enddo
      end
    
      
      subroutine en_cl(xx,kk,ww,dd,d)
      implicit none
!     returns 
!     1.: lower index and lower weight 
!     2.: upper index and upper weight
!     k: place
!     w: weight
!     d: rank
      INTEGER i,d
      INTEGER kk(d,2),dd(d)
      double precision xx(d),ww(d,2)
        do i=1,d
            kk(i,1) = max(0,idint(xx(i)))
            kk(i,1) = min(dd(i)-1,kk(i,1))
            kk(i,2) = min(dd(i)-1,kk(i,1)+1)
        enddo  
        !weights
        do i=1,d
            ww(i,2)=(xx(i)-kk(i,1))
            ww(i,1)=1.d0-ww(i,2)
        enddo
        !fortran style 
        do i=1,d
            kk(i,1) = kk(i,1)+1
            kk(i,2) = kk(i,2)+1
        enddo        
      end
      
      
      subroutine check1d(xx,yy,n)
CF2PY INTENT(IN) :: xx
CF2PY INTENT(OUT) :: yy
CF2PY INTENT(HIDE) :: n
CF2PY DOUBLE :: xx(n),yy(n)
      implicit none
      INTEGER n,i
      real*8 xx(n),yy(n)
      do i=1,n
        yy(i)=xx(i)
      enddo
      end

      subroutine check2d(xx,yy,n1,n2)
CF2PY INTENT(IN) :: xx
CF2PY INTENT(OUT) :: yy200
CF2PY INTENT(HIDE) :: n1,n2
CF2PY DOUBLE :: xx(n1,n2),yy
      implicit none
      INTEGER n1,n2,i1,i2
      real*8 xx(n1,n2),yy
      do i1=1,n1
      do i2=1,n2
        yy=xx(i1,i2)
      enddo
      enddo
      end     

      subroutine check3d(xx,yy,n1,n2,n3)
CF2PY INTENT(IN) :: xx
CF2PY INTENT(OUT) :: yy
CF2PY INTENT(HIDE) :: n1,n2,n3
CF2PY DOUBLE :: xx(n1,n2,n3),yy
      implicit none
      INTEGER n1,n2,n3,i1,i2,i3
      real*8 xx(n1,n2,n3),yy
      do i1=1,n1
      do i2=1,n2
      do i3=1,n3
        yy=xx(i1,i2,i3)
      enddo
      enddo
      enddo
      end     

      subroutine check4d(xx,yy,n1,n2,n3,n4)
CF2PY INTENT(IN) :: xx
CF2PY INTENT(OUT) :: yy
CF2PY INTENT(HIDE) :: n1,n2,n3,n4
CF2PY DOUBLE :: xx(n1,n2,n3,n4),yy
      implicit none
      INTEGER n1,n2,n3,n4,i1,i2,i3,i4
      real*8 xx(n1,n2,n3,n4),yy
      do i1=1,n1
      do i2=1,n2
      do i3=1,n3
      do i4=1,n4
        yy=xx(i1,i2,i3,i4)
      enddo
      enddo
      enddo
      enddo
      end     
      
      subroutine check5d(xx,yy,n1,n2,n3,n4,n5)
CF2PY INTENT(IN) :: xx
CF2PY INTENT(OUT) :: yy
CF2PY INTENT(HIDE) :: n1,n2,n3,n4,n5
CF2PY DOUBLE :: xx(n1,n2,n3,n4,n5),yy
      implicit none
      INTEGER n1,n2,n3,n4,n5,i1,i2,i3,i4,i5
      real*8 xx(n1,n2,n3,n4,n5),yy
      do i1=1,n1
      do i2=1,n2
      do i3=1,n3
      do i4=1,n4
      do i5=1,n5
        yy=xx(i1,i2,i3,i4,i5)
      enddo
      enddo
      enddo
      enddo
      enddo
      end     

      
      
      SUBROUTINE interpol_1(xx,lut,out,d1)
      implicit none

C     input is index
C
CF2PY INTENT(IN) :: lut, xx
CF2PY INTENT(OUT) :: out
CF2PY INTENT(HIDE) :: d1
CF2PY DOUBLE :: lut(d1)
CF2PY DOUBLE :: out
CF2PY DOUBLE :: xx(1)
      INTEGER d1
      INTEGER j1
      INTEGER kk(1,2),dd(1)
      DOUBLE PRECISION lut(d1)
      DOUBLE PRECISION out,xx(1)
      DOUBLE PRECISION ww(1,2)
      DOUBLE PRECISION wgt
      
      
      !shape of LUT
      dd(1)=d1
      
      !positions
      call en_cl(xx,kk,ww,dd,1)
        !define output
        out = 0.d0        
        !doit   
        DO 10 j1 = 1, 2
            wgt = ww(1,j1)
            out = out + lut(kk(1,j1))*wgt
10       CONTINUE
      end

      SUBROUTINE interpol_nan_1(xx,lut,out,d1)
      implicit none

C     input is index
C
CF2PY INTENT(IN) :: lut, xx
CF2PY INTENT(OUT) :: out
CF2PY INTENT(HIDE) :: d1
CF2PY DOUBLE :: lut(d1)
CF2PY DOUBLE :: out
CF2PY DOUBLE :: xx(1)
      INTEGER d1
      INTEGER j1
      INTEGER kk(1,2),dd(1)
      DOUBLE PRECISION lut(d1)
      DOUBLE PRECISION out,xx(1)
      DOUBLE PRECISION ww(1,2)
      DOUBLE PRECISION wgt,swgt,ll
      
      
      !shape of LUT
      dd(1)=d1
      
      !positions
      call en_cl(xx,kk,ww,dd,1)
        !define output
        out = 0.d0
        swgt= 0.d0
        !doit   
        DO 10 j1 = 1, 2
            ll=lut(kk(1,j1))
            if (.not. isnan(ll)) then
              wgt = ww(1,j1)
              out = out + ll*wgt
              swgt = swgt +wgt
            endif  
10       CONTINUE
        out=out/swgt
      end

      SUBROUTINE interpol_1pn(xx,lut,out,d1,d2)
      implicit none

C     input is index
C
CF2PY INTENT(IN) :: lut, xx
CF2PY INTENT(OUT) :: out
CF2PY INTENT(HIDE) :: d1,d2
CF2PY DOUBLE :: lut(d1,d2)
CF2PY DOUBLE :: out(d2)
CF2PY DOUBLE :: xx(1)
      INTEGER d1,d2
      INTEGER j1
      INTEGER kk(1,2),dd(1)
      DOUBLE PRECISION lut(d1,d2)
      DOUBLE PRECISION out(d2),xx(1)
      DOUBLE PRECISION ww(1,2)
      DOUBLE PRECISION wgt

        !shape of LUT
        dd(1)=d1
      
        !positions
        call en_cl(xx,kk,ww,dd,1)
        !define output
        out(:) = 0.d0        
        !doit   
        DO 10 j1 = 1, 2
            wgt = ww(1,j1)
            out(:) = out(:) + lut(kk(1,j1),:)*wgt
10      CONTINUE
      end


      SUBROUTINE interpol_2(xx,lut,out,d1,d2)
      implicit none

C     input is index
C
CF2PY INTENT(IN) :: lut, xx
CF2PY INTENT(OUT) :: out
CF2PY INTENT(HIDE) :: d1,d2
CF2PY DOUBLE :: lut(d1,d2)
CF2PY DOUBLE :: out
CF2PY DOUBLE :: xx(2)
      INTEGER d1, d2
      INTEGER j1, j2
      INTEGER kk(2,2),dd(2)
      DOUBLE PRECISION lut(d1,d2)
      DOUBLE PRECISION out,xx(2)
      DOUBLE PRECISION ww(2,2)
      DOUBLE PRECISION wgt
      
      
      !shape of LUT
      dd(1)=d1
      dd(2)=d2
      
      !positions
      call en_cl(xx,kk,ww,dd,2)      
        !define output
        out = 0.d0        
        !doit   
        DO 20 j2 = 1, 2
        DO 10 j1 = 1, 2
            wgt = ww(1,j1)*ww(2,j2)
            out = out + lut(kk(1,j1),kk(2,j2))*wgt
10       CONTINUE
20       CONTINUE
      end

      SUBROUTINE interpol_nan_2(xx,lut,out,d1,d2)
      implicit none

C     input is index
C
CF2PY INTENT(IN) :: lut, xx
CF2PY INTENT(OUT) :: out
CF2PY INTENT(HIDE) :: d1,d2
CF2PY DOUBLE :: lut(d1,d2)
CF2PY DOUBLE :: out
CF2PY DOUBLE :: xx(2)
      INTEGER d1, d2
      INTEGER j1, j2
      INTEGER kk(2,2),dd(2)
      DOUBLE PRECISION lut(d1,d2)
      DOUBLE PRECISION out,xx(2)
      DOUBLE PRECISION ww(2,2)
      DOUBLE PRECISION wgt,swgt,ll
      
      
      !shape of LUT
      dd(1)=d1
      dd(2)=d2
      
      !positions
      call en_cl(xx,kk,ww,dd,2)      
        !define output
        out = 0.d0
        swgt= 0.d0
        !doit   
        DO 20 j2 = 1, 2
        DO 10 j1 = 1, 2
            ll=lut(kk(1,j1),kk(2,j2))
            if (.not. isnan(ll)) then
              wgt = ww(1,j1)*ww(2,j2)
              out = out + ll*wgt
              swgt=swgt+wgt
            endif  
10       CONTINUE
20       CONTINUE
        out=out/swgt
      end
      
      
      
      
      SUBROUTINE interpol_2pn(xx,lut,out,d1,d2,d3)
      implicit none

C     input is index
C
CF2PY INTENT(IN) :: lut, xx
CF2PY INTENT(OUT) :: out
CF2PY INTENT(HIDE) :: d1,d2,d3
CF2PY DOUBLE :: lut(d1,d2,d3)
CF2PY DOUBLE :: out
CF2PY DOUBLE :: xx(2)
      INTEGER d1, d2, d3
      INTEGER j1, j2
      INTEGER kk(2,2),dd(2)
      DOUBLE PRECISION lut(d1,d2,d3)
      DOUBLE PRECISION out(d3),xx(2)
      DOUBLE PRECISION ww(2,2)
      DOUBLE PRECISION wgt
      
      
      !shape of LUT
      dd(1)=d1
      dd(2)=d2
      
      !positions
      call en_cl(xx,kk,ww,dd,2)      
        !define output
        out(:) = 0.d0        
        !doit   
        DO 20 j2 = 1, 2
        DO 10 j1 = 1, 2
            wgt = ww(1,j1)*ww(2,j2)
            out(:) = out(:) + lut(kk(1,j1),kk(2,j2),:)*wgt
10       CONTINUE
20       CONTINUE
      end
      

      
      
      SUBROUTINE interpol_3(xx,lut,out,d1,d2,d3)
      implicit none

C     input is index
C
CF2PY INTENT(IN) :: lut, xx
CF2PY INTENT(OUT) :: out
CF2PY INTENT(HIDE) :: d1,d2,d3
CF2PY DOUBLE :: lut(d1,d2,d3)
CF2PY DOUBLE :: out
CF2PY DOUBLE :: xx(3)
      INTEGER d1, d2, d3
      INTEGER j1, j2, j3
      INTEGER kk(3,2),dd(3)
      DOUBLE PRECISION lut(d1,d2,d3)
      DOUBLE PRECISION out,xx(3)
      DOUBLE PRECISION ww(3,2)
      DOUBLE PRECISION wgt
      
      
      !shape of LUT
      dd(1)=d1
      dd(2)=d2
      dd(3)=d3
      
      !positions
      call en_cl(xx,kk,ww,dd,3)      
        !define output
        out = 0.d0        
        !doit   
        DO 30 j3 = 1, 2
        DO 20 j2 = 1, 2
        DO 10 j1 = 1, 2
            wgt = ww(1,j1)*ww(2,j2)*ww(3,j3)
            out = out + lut(kk(1,j1),kk(2,j2),kk(3,j3))*wgt
10       CONTINUE
20       CONTINUE
30       CONTINUE
      end

      SUBROUTINE interpol_nan_3(xx,lut,out,d1,d2,d3)
      implicit none

C     input is index
C
CF2PY INTENT(IN) :: lut, xx
CF2PY INTENT(OUT) :: out
CF2PY INTENT(HIDE) :: d1,d2,d3
CF2PY DOUBLE :: lut(d1,d2,d3)
CF2PY DOUBLE :: out
CF2PY DOUBLE :: xx(3)
      INTEGER d1, d2, d3
      INTEGER j1, j2, j3
      INTEGER kk(3,2),dd(3)
      DOUBLE PRECISION lut(d1,d2,d3)
      DOUBLE PRECISION out,xx(3)
      DOUBLE PRECISION ww(3,2)
      DOUBLE PRECISION wgt,swgt,ll
      
      
      !shape of LUT
      dd(1)=d1
      dd(2)=d2
      dd(3)=d3
      
      !positions
      call en_cl(xx,kk,ww,dd,3)      
        !define output
        out = 0.d0
        swgt=0.d0
        !doit   
        DO 30 j3 = 1, 2
        DO 20 j2 = 1, 2
        DO 10 j1 = 1, 2
            ll=lut(kk(1,j1),kk(2,j2),kk(3,j3))
            if (.not. isnan(ll)) then
              wgt = ww(1,j1)*ww(2,j2)*ww(3,j3)
              out = out + ll*wgt
              swgt=swgt+wgt
            endif  
10       CONTINUE
20       CONTINUE
30       CONTINUE
         out=out/swgt
      end

      SUBROUTINE interpol_3pn(xx,lut,out,d1,d2,d3,d4)
      implicit none

C     input is index
C
CF2PY INTENT(IN) :: lut, xx
CF2PY INTENT(OUT) :: out
CF2PY INTENT(HIDE) :: d1,d2,d3,d4
CF2PY DOUBLE :: lut(d1,d2,d3,d4)
CF2PY DOUBLE :: out(d4)
CF2PY DOUBLE :: xx(3)
      INTEGER d1, d2, d3, d4
      INTEGER j1, j2, j3
      INTEGER kk(3,2),dd(3)
      DOUBLE PRECISION lut(d1,d2,d3,d4)
      DOUBLE PRECISION out(d4),xx(3)
      DOUBLE PRECISION ww(3,2)
      DOUBLE PRECISION wgt
      
      
      !shape of LUT
      dd(1)=d1
      dd(2)=d2
      dd(3)=d3
      
      !positions
      call en_cl(xx,kk,ww,dd,3)      
        !define output
        out(:) = 0.d0        
        !doit   
        DO 30 j3 = 1, 2
        DO 20 j2 = 1, 2
        DO 10 j1 = 1, 2
            wgt = ww(1,j1)*ww(2,j2)*ww(3,j3)
            out(:) = out(:) + lut(kk(1,j1),kk(2,j2),kk(3,j3),:)*wgt
10      CONTINUE
20      CONTINUE
30      CONTINUE
      end

      
      
      SUBROUTINE interpol_4(xx,lut,out,d1,d2,d3,d4)
      implicit none

C     input is index
C
CF2PY INTENT(IN) :: lut, xx
CF2PY INTENT(OUT) :: out
CF2PY INTENT(HIDE) :: d1,d2,d3,d4
CF2PY DOUBLE :: lut(d1,d2,d3,d4)
CF2PY DOUBLE :: out
CF2PY DOUBLE :: xx(4)
      INTEGER d1, d2, d3, d4
      INTEGER j1, j2, j3, j4
      INTEGER kk(4,2),dd(4)
      DOUBLE PRECISION lut(d1,d2,d3,d4)
      DOUBLE PRECISION out,xx(4)
      DOUBLE PRECISION ww(4,2)
      DOUBLE PRECISION wgt
      
      
      !shape of LUT
      dd(1)=d1
      dd(2)=d2
      dd(3)=d3
      dd(4)=d4
      
      !positions
      call en_cl(xx,kk,ww,dd,4)      
        !define output
        out = 0.d0        
        !doit   
        DO 40 j4 = 1, 2
        DO 30 j3 = 1, 2
        DO 20 j2 = 1, 2
        DO 10 j1 = 1, 2
            wgt = ww(1,j1)*ww(2,j2)*ww(3,j3)*ww(4,j4)
            out = out + lut(kk(1,j1),kk(2,j2),kk(3,j3),kk(4,j4))*wgt
10       CONTINUE
20       CONTINUE
30       CONTINUE
40       CONTINUE
      end

      SUBROUTINE interpol_nan_4(xx,lut,out,d1,d2,d3,d4)
      implicit none

C     input is index
C
CF2PY INTENT(IN) :: lut, xx
CF2PY INTENT(OUT) :: out
CF2PY INTENT(HIDE) :: d1,d2,d3,d4
CF2PY DOUBLE :: lut(d1,d2,d3,d4)
CF2PY DOUBLE :: out
CF2PY DOUBLE :: xx(4)
      INTEGER d1, d2, d3, d4
      INTEGER j1, j2, j3, j4
      INTEGER kk(4,2),dd(4)
      DOUBLE PRECISION lut(d1,d2,d3,d4)
      DOUBLE PRECISION out,xx(4)
      DOUBLE PRECISION ww(4,2)
      DOUBLE PRECISION wgt,swgt,ll
      
      
      !shape of LUT
      dd(1)=d1
      dd(2)=d2
      dd(3)=d3
      dd(4)=d4
      
      !positions
      call en_cl(xx,kk,ww,dd,4)      
        !define output
        out = 0.d0
        swgt =0.d0
        !doit   
        DO 40 j4 = 1, 2
        DO 30 j3 = 1, 2
        DO 20 j2 = 1, 2
        DO 10 j1 = 1, 2
            ll=lut(kk(1,j1),kk(2,j2),kk(3,j3),kk(4,j4))
            if (.not. isnan(ll)) then
             wgt = ww(1,j1)*ww(2,j2)*ww(3,j3)*ww(4,j4)
             out = out + ll*wgt
             swgt= swgt+wgt
            endif 
10       CONTINUE
20       CONTINUE
30       CONTINUE
40       CONTINUE
         out=out/swgt
      end

      SUBROUTINE interpol_4pn(xx,lut,out,d1,d2,d3,d4,d5)
      implicit none

C     input is index
C
CF2PY INTENT(IN) :: lut, xx
CF2PY INTENT(OUT) :: out
CF2PY INTENT(HIDE) :: d1,d2,d3,d4,d5
CF2PY DOUBLE :: lut(d1,d2,d3,d4,d5)
CF2PY DOUBLE :: out
CF2PY DOUBLE :: xx(4)
      INTEGER d1, d2, d3, d4, d5
      INTEGER j1, j2, j3, j4
      INTEGER kk(4,2),dd(4)
      DOUBLE PRECISION lut(d1,d2,d3,d4,d5)
      DOUBLE PRECISION out(d5),xx(4)
      DOUBLE PRECISION ww(4,2)
      DOUBLE PRECISION wgt
      
      
      !shape of LUT
      dd(1)=d1
      dd(2)=d2
      dd(3)=d3
      dd(4)=d4
      
      !positions
      call en_cl(xx,kk,ww,dd,4)      
        !define output
        out(:) = 0.d0        
        !doit   
        DO 40 j4 = 1, 2
        DO 30 j3 = 1, 2
        DO 20 j2 = 1, 2
        DO 10 j1 = 1, 2
          wgt = ww(1,j1)*ww(2,j2)*ww(3,j3)*ww(4,j4)
          out(:) = out(:) + 
     &             lut(kk(1,j1),kk(2,j2),kk(3,j3),kk(4,j4),:)*wgt
10      CONTINUE
20      CONTINUE
30      CONTINUE
40      CONTINUE
      end
      

      
      
      SUBROUTINE interpol_5(xx,lut,out,d1,d2,d3,d4,d5)
      implicit none

C     input is index
C
CF2PY INTENT(IN) :: lut, xx
CF2PY INTENT(OUT) :: out
CF2PY INTENT(HIDE) :: d1,d2,d3,d4,d5
CF2PY DOUBLE :: lut(d1,d2,d3,d4,d5)
CF2PY DOUBLE :: out
CF2PY DOUBLE :: xx(5)
      INTEGER d1, d2, d3, d4, d5
      INTEGER j1, j2, j3, j4, j5
      INTEGER kk(5,2),dd(5)
      DOUBLE PRECISION lut(d1,d2,d3,d4,d5)
      DOUBLE PRECISION out,xx(5)
      DOUBLE PRECISION ww(5,2)
      DOUBLE PRECISION wgt
      
      
      !shape of LUT
      dd(1)=d1
      dd(2)=d2
      dd(3)=d3
      dd(4)=d4
      dd(5)=d5
      
      !positions
      call en_cl(xx,kk,ww,dd,5)      
        !define output
        out = 0.d0        
        !doit   
        DO 50 j5 = 1, 2
        DO 40 j4 = 1, 2
        DO 30 j3 = 1, 2
        DO 20 j2 = 1, 2
        DO 10 j1 = 1, 2
         wgt = ww(1,j1)*ww(2,j2)*ww(3,j3)*ww(4,j4)*ww(5,j5)
         out = out + lut(kk(1,j1),kk(2,j2),kk(3,j3),kk(4,j4)
     &                  ,kk(5,j5))*wgt
10       CONTINUE
20       CONTINUE
30       CONTINUE
40       CONTINUE
50       CONTINUE
      end

      SUBROUTINE interpol_5pn(xx,lut,out,d1,d2,d3,d4,d5,d6)
      implicit none

C     input is index
C
CF2PY INTENT(IN) :: lut, xx
CF2PY INTENT(OUT) :: out
CF2PY INTENT(HIDE) :: d1,d2,d3,d4,d5,d6
CF2PY DOUBLE :: lut(d1,d2,d3,d4,d5,d6)
CF2PY DOUBLE :: out
CF2PY DOUBLE :: xx(5)
      INTEGER d1, d2, d3, d4, d5, d6
      INTEGER j1, j2, j3, j4, j5
      INTEGER kk(5,2),dd(5)
      DOUBLE PRECISION lut(d1,d2,d3,d4,d5,d6)
      DOUBLE PRECISION out(d6),xx(5)
      DOUBLE PRECISION ww(5,2)
      DOUBLE PRECISION wgt
      
      
      !shape of LUT
      dd(1)=d1
      dd(2)=d2
      dd(3)=d3
      dd(4)=d4
      dd(5)=d5
      
      !positions
      call en_cl(xx,kk,ww,dd,5)      
        !define output
        out(:) = 0.d0        
        !doit   
        DO 50 j5 = 1, 2
        DO 40 j4 = 1, 2
        DO 30 j3 = 1, 2
        DO 20 j2 = 1, 2
        DO 10 j1 = 1, 2
         wgt = ww(1,j1)*ww(2,j2)*ww(3,j3)*ww(4,j4)*ww(5,j5)
         out(:) = out(:) + lut(kk(1,j1),kk(2,j2),kk(3,j3),kk(4,j4)
     &                  ,kk(5,j5),:)*wgt
10       CONTINUE
20       CONTINUE
30       CONTINUE
40       CONTINUE
50       CONTINUE
      end

      
      
      SUBROUTINE interpol_6(xx,lut,out,d1,d2,d3,d4,d5,d6)
      implicit none

C     input is index
C
CF2PY INTENT(IN) :: lut, xx
CF2PY INTENT(OUT) :: out
CF2PY INTENT(HIDE) :: d1,d2,d3,d4,d5,d6
CF2PY DOUBLE :: lut(d1,d2,d3,d4,d5,d6)
CF2PY DOUBLE :: out
CF2PY DOUBLE :: xx(6)
      INTEGER d1, d2, d3, d4, d5, d6
      INTEGER j1, j2, j3, j4, j5, j6
      INTEGER kk(6,2),dd(6)
      DOUBLE PRECISION lut(d1,d2,d3,d4,d5,d6)
      DOUBLE PRECISION out,xx(6)
      DOUBLE PRECISION ww(6,2)
      DOUBLE PRECISION wgt
      
      
      !shape of LUT
      dd(1)=d1
      dd(2)=d2
      dd(3)=d3
      dd(4)=d4
      dd(5)=d5
      dd(6)=d6
      
      !positions
      call en_cl(xx,kk,ww,dd,6)      
        !define output
        out = 0.d0        
        !doit   
        DO 60 j6 = 1, 2
        DO 50 j5 = 1, 2
        DO 40 j4 = 1, 2
        DO 30 j3 = 1, 2
        DO 20 j2 = 1, 2
        DO 10 j1 = 1, 2
         wgt = ww(1,j1)*ww(2,j2)*ww(3,j3)*ww(4,j4)*ww(5,j5)
     &         * ww(6,j6)
         out = out + lut(kk(1,j1),kk(2,j2),kk(3,j3),kk(4,j4)
     &                  ,kk(5,j5),kk(6,j6))*wgt
10       CONTINUE
20       CONTINUE
30       CONTINUE
40       CONTINUE
50       CONTINUE
60       CONTINUE
      end

      SUBROUTINE interpol_6pn(xx,lut,out,d1,d2,d3,d4,d5,d6,d7)
      implicit none

C     input is index
C
CF2PY INTENT(IN) :: lut, xx
CF2PY INTENT(OUT) :: out
CF2PY INTENT(HIDE) :: d1,d2,d3,d4,d5,d6,d7
CF2PY DOUBLE :: lut(d1,d2,d3,d4,d5,d6,d7)
CF2PY DOUBLE :: out(d7)
CF2PY DOUBLE :: xx(6)
      INTEGER d1, d2, d3, d4, d5, d6, d7
      INTEGER j1, j2, j3, j4, j5, j6
      INTEGER kk(6,2),dd(6)
      DOUBLE PRECISION lut(d1,d2,d3,d4,d5,d6,d7)
      DOUBLE PRECISION out(d7),xx(6)
      DOUBLE PRECISION ww(6,2)
      DOUBLE PRECISION wgt
      
      
      !shape of LUT
      dd(1)=d1
      dd(2)=d2
      dd(3)=d3
      dd(4)=d4
      dd(5)=d5
      dd(6)=d6
      
      !positions
      call en_cl(xx,kk,ww,dd,6)      
        !define output
        out(:) = 0.d0        
        !doit   
        DO 60 j6 = 1, 2
        DO 50 j5 = 1, 2
        DO 40 j4 = 1, 2
        DO 30 j3 = 1, 2
        DO 20 j2 = 1, 2
        DO 10 j1 = 1, 2
         wgt = ww(1,j1)*ww(2,j2)*ww(3,j3)*ww(4,j4)*ww(5,j5)
     &         * ww(6,j6)
         out(:) = out(:) + lut(kk(1,j1),kk(2,j2),kk(3,j3),kk(4,j4)
     &                  ,kk(5,j5),kk(6,j6),:)*wgt
10       CONTINUE
20       CONTINUE
30       CONTINUE
40       CONTINUE
50       CONTINUE
60       CONTINUE
      end

      
      
      SUBROUTINE interpol_7(xx,lut,out,d1,d2,d3,d4,d5,d6,d7)
      implicit none

C     input is index
C
CF2PY INTENT(IN) :: lut, xx
CF2PY INTENT(OUT) :: out
CF2PY INTENT(HIDE) :: d1,d2,d3,d4,d5,d6,d7
CF2PY DOUBLE :: lut(d1,d2,d3,d4,d5,d6,d7)
CF2PY DOUBLE :: out
CF2PY DOUBLE :: xx(7)
      INTEGER d1, d2, d3, d4, d5, d6, d7
      INTEGER j1, j2, j3, j4, j5, j6, j7
      INTEGER kk(7,2),dd(7)
      DOUBLE PRECISION lut(d1,d2,d3,d4,d5,d6,d7)
      DOUBLE PRECISION out,xx(7)
      DOUBLE PRECISION ww(7,2)
      DOUBLE PRECISION wgt
      
      
      !shape of LUT
      dd(1)=d1
      dd(2)=d2
      dd(3)=d3
      dd(4)=d4
      dd(5)=d5
      dd(6)=d6
      dd(7)=d7
      
      !positions
      call en_cl(xx,kk,ww,dd,7)      
        !define output
        out = 0.d0        
        !doit   
        DO 70 j7 = 1, 2
        DO 60 j6 = 1, 2
        DO 50 j5 = 1, 2
        DO 40 j4 = 1, 2
        DO 30 j3 = 1, 2
        DO 20 j2 = 1, 2
        DO 10 j1 = 1, 2
         wgt = ww(1,j1)*ww(2,j2)*ww(3,j3)*ww(4,j4)*ww(5,j5)
     &         * ww(6,j6) * ww(7,j7)
         out = out + lut(kk(1,j1),kk(2,j2),kk(3,j3),kk(4,j4)
     &                  ,kk(5,j5),kk(6,j6),kk(7,j7))*wgt
10       CONTINUE
20       CONTINUE
30       CONTINUE
40       CONTINUE
50       CONTINUE
60       CONTINUE
70       CONTINUE
      end
      
            
    
      subroutine permute_two(n,b,out)
      implicit none
      integer n,b,i
      integer out(b)
      logical lll
      do i=0,b-1
      !no implicit conversion in fortran :-(
        lll = btest(n-1,i)
        if ( lll ) then
            out(b-i)= 2
        else 
            out(b-i)= 1
        endif    
      enddo
      end
      
      SUBROUTINE indexto1(jj,dd,rank,out)
      implicit none
      INTEGER rank
      INTEGER*8 i,mul,out
      INTEGER jj(rank)
      INTEGER*8 dd(rank)
      out=jj(rank)-1   
      mul=1
      do 10 i=1,rank-1 
        mul=mul*dd(rank-i+1)
        out=out+mul*(jj(rank-i)-1)
10    continue
      out=out+1
      end
  
     
      
      SUBROUTINE interpol_n(xx,lut,dd,out,si,di)
      implicit none

C     input is index
C
CF2PY INTENT(IN) :: lut,xx,dd,si
CF2PY INTENT(OUT) :: out
CF2PY INTENT(HIDE) :: si,di
CF2PY DOUBLE :: lut(si)
CF2PY DOUBLE :: out
CF2PY DOUBLE :: xx(di)
CF2PY INTEGER :: si,di
CF2PY INTEGER*8 :: dd(di)
!       INTEGER j1, j2, j3, j4, j5, j6, j7, j8, i,j, di
      INTEGER i,j, di
      INTEGER kk(di,2),dl(di),nd_idx(di),jj(di)
      INTEGER*8 dd(di),idx,si
      DOUBLE PRECISION lut(si)
      DOUBLE PRECISION out,xx(di)
      DOUBLE PRECISION ww(di,2)
      DOUBLE PRECISION wgt
      
      
      do i=1,di
         dl(i)=long(dd(i))
      enddo      
      call en_cl(xx,kk,ww,dl,di)

      out = 0.d0        
      do i=1,2**di
        call permute_two(i,di,jj)
        wgt=1.d0 
        do j=1,di
                nd_idx(j)=kk(j,jj(j))
                wgt = wgt*ww(j,jj(j))
        enddo
        call indexto1(nd_idx,dd,di,idx) 
        out = out + lut(idx)*wgt 
      enddo      
      end

      
      
      
      SUBROUTINE interpol_npn(xx,lut,dd,out,si,di,du)
      implicit none

C     input is index
C
CF2PY INTENT(IN) :: lut,xx,dd,si
CF2PY INTENT(OUT) :: out
CF2PY INTENT(HIDE) :: si,di
CF2PY DOUBLE :: lut(si,du)
CF2PY DOUBLE :: out(du)
CF2PY DOUBLE :: xx(di)
CF2PY INTEGER :: si,di,du
CF2PY INTEGER*8 :: dd(di)
      INTEGER i,j, di, du
      INTEGER kk(di,2),dl(di),nd_idx(di),jj(di)
      INTEGER*8 dd(di),idx,si
      DOUBLE PRECISION lut(si,du)
      DOUBLE PRECISION out(du),xx(di)
      DOUBLE PRECISION ww(di,2)
      DOUBLE PRECISION wgt
      
      
      do i=1,di
         dl(i)=long(dd(i))
      enddo      
      call en_cl(xx,kk,ww,dl,di)

      out(:) = 0.d0        
      do i=1,2**di
        call permute_two(i,di,jj)
        wgt=1.d0 
        do j=1,di
                nd_idx(j)=kk(j,jj(j))
                wgt = wgt*ww(j,jj(j))
        enddo
        call indexto1(nd_idx,dd,di,idx) 
        out(:) = out(:) + lut(idx,:)*wgt 
      enddo      
      end

       