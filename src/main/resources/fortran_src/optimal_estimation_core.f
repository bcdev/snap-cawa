      subroutine test(x,y1,y2,d)
      implicit none
c     test
cf2py intent(in) :: x
cf2py intent(out) :: y1,y2
cf2py intent(hide) :: d
cf2py double :: x(d),y1(d),y2(d)
      integer i
      integer d
      double precision x(d),y1(d),y2(d)
      
      do 100 i=1,d
        y1(i)=x(i)*2.d0
        y2(i)=x(i)*3.d0
100   enddo
      end

      
      subroutine dot(x,y,z,dx1,dxy,dy2)
cf2py intent(in) :: x,y
cf2py intent(out) :: z
cf2py intent(hide) :: dx1,dxy,dy2
cf2py double :: x(dx1,dxy),y(dxy,dy2),z(dx1,dy2)
      implicit none
      integer dx1,dxy,dy2
      integer ix1,ixy,iy2
      double precision x(dx1,dxy),y(dxy,dy2),z(dx1,dy2)
      
      do 100 ix1=1,dx1
      do 200 iy2=1,dy2
        z(ix1,iy2)=0.d0
        do 300 ixy=1,dxy
            z(ix1,iy2)=z(ix1,iy2)+ x(ix1,ixy)*y(ixy,iy2)      
300     enddo 
200   enddo
100   enddo
      
      end
      
    
      subroutine inverse(a,x,n)       
        ! invert matrix using  gauss elemination
        ! -----------------------------------------------------
cf2py intent(in) :: a
cf2py intent(out) :: x
cf2py intent(hide) :: n
cf2py double :: a(n,n),x(n,n)        
        implicit none
        integer :: n  
        real*8 :: a(n,n),x(n,n)
        ! - - - local variables - - -
        real*8 :: b(n,n),c,d,temp(n)
        integer :: i,j,k,m,imax(1),ipvt(n)
    ! - - - - - - - - - - - - - -      
        b=a
        ipvt =(/(i,i=1,n) /)
        do 100 k=1,n
            imax=maxloc(abs(b(k:n,k)))
            m=k-1+imax(1)

            if(m /= k) then
                ipvt((/m,k/) )=ipvt((/k,m/) )
                b((/m,k/),:)=b((/k,m/),:)
            end if
            d=1.d0/b(k,k)
            temp=b(:,k)
            do 200 j=1,n
                c=b(k,j)*d
                b(:,j)=b(:,j)-temp*c
                b(k,j)=c
200         end do
            b(:,k)=temp*(-d)
            b(k,k)=d
100     end do
        x(:,ipvt)=b
        end 
            
      subroutine left_inverse(a,x,n,m)       
cf2py intent(in) :: a
cf2py intent(out) :: x
cf2py intent(hide) :: n
cf2py double :: a(n,m),x(n,m)        
        implicit none
        integer :: n,m   
        real*8 :: a(n,m),x(m,n)
        ! - - - local variables - - -
        real*8 :: at(m,n),ata(m,m),atai(m,m)
        at=transpose(a)
        call dot(at,a,ata,m,n,m)
!         print *,ata
        call inverse(ata,atai,m)
!         print *,atai
        call dot(atai,at,x,m,m,n)
        end
        
      subroutine clipper(a,b,x,y,n)
cf2py intent(in) :: a,b,x
cf2py intent(out) :: y
cf2py intent(hide) :: n
cf2py double :: a(n),b(n),x(n),y(n)        
        implicit none
        integer :: n,i   
        real*8 :: a(n),b(n),x(n),y(n)
        y=x
        do i=1,n
            if (x(i).lt.a(i)) then
              y(i)=a(i)
              continue
            endif
            if (x(i).gt.b(i)) then
              y(i)=b(i)
            endif        
        enddo      
      end

      
      
      subroutine norm_error_weighted_x(ix, sri,norm,n)
cf2py intent(in) :: ix,sri
cf2py intent(out) :: norm
cf2py intent(hide) :: n     
cf2py double :: ix(n),sri(n,n),norm      
cf2py integer :: n
        implicit none
        integer :: n,i  
        real*8 :: ix(n),sri(n,n),norm
        real*8 :: ixt(1,n),ix1(n,1),nn(1,1)
        real*8 :: sri_ix(n,n)
        do i=1,n
          ixt(1,i)= ix(i) 
          ix1(i,1)= ix(i)
        enddo
        call dot(sri,ix1,sri_ix,n,n,1)
        call dot(ixt,sri_ix,nn,1,n,1)
        norm=nn(1,1)
      end  
      subroutine norm_y(y, norm,m)
cf2py intent(in) :: y
cf2py intent(out) :: norm
cf2py intent(hide) :: m     
cf2py double :: y(m)
cf2py integer :: m
        implicit none
        integer :: m,i  
        real*8 :: y(m),norm
        norm=0.d0
        do i=1,m
            norm=norm+y(i)*y(i)
        enddo
        norm=norm/dble(m)
      end   
      
! #######################################################################
! #######################################################################
! #######################################################################
! #######################################################################
! ###Gauss Newton Operator      
      subroutine newton_operator(a, b, x, y, k
     %                       , cnx, incr_x,sri,sr,n,m)  
cf2py intent(in) :: a,b,x,y,k
cf2py intent(out) :: cnx,incr_x,sri,sr
cf2py intent(hide) :: n,m 
cf2py integer :: n,m
cf2py double :: a(n),b(n),x(n),y(m)
cf2py double :: k(m,n),cnx(n),incr_x(n),sei(m,m),se(m,m)    
        implicit none
        integer :: n,m,i,j  
        real*8 :: a(n),b(n),x(n),y(m),k(m,n),cnx(n)
        real*8 :: sri(n,n),sr(n,n)
        ! - - - local variables - - -
        real*8 :: ki(n,m),incr_x(n),nx(n)
        call left_inverse(k,ki,m,n)
        call dot(ki,y,incr_x,n,m,1)
        do i=1,n
            nx(i)=x(i)-incr_x(i)
        enddo
        call clipper(a,b,nx,cnx,n)
        do i=1,n
        do j=1,n
            sr(i,j)=0.d0
            sri(i,j)=0.d0
        enddo
        enddo
      end
      
      subroutine newton_gain_aver_cost(x, y, k, gain, aver
     %                                    ,cost,n,m)
cf2py intent(in) ::   x, y, k 
cf2py intent(out) :: gain, aver, cost 
cf2py intent(hide) :: n,m 
cf2py integer :: n,m
cf2py double :: x(n),y(m),k(m,n)
cf2py double :: gain(n,m), aver(n,n),cost(1,1)
        implicit none
        integer :: n,m,i,j
        real*8 :: x(n),y(m)
        real*8 :: k(m,n),gain(n,m),aver(n,n)
        real*8 :: cost(1,1),yt(1,m)
        call left_inverse(k,gain,m,n)
        do i=1,n
            do j=1,n
                aver(i,j)=0.d0
            enddo
            aver(i,i)=1.d0
        enddo
        do i=1,m
             yt(1,i)=y(i)
        enddo
        call dot(yt,y,cost,1,m,1)
      end

      
! #######################################################################
! #######################################################################
! #######################################################################
! #######################################################################
! ###Gauss Newton Operator with measurement error
      subroutine newton_operator_with_se(a, b, x, y, k, sei
     %                        , cnx, incr_x,sri,sr,n,m)  
cf2py intent(in) :: a,b,x,y,k,sei
cf2py intent(out) :: cnx,incr_x,sri,sr
cf2py intent(hide) :: n,m 
cf2py integer :: n,m
cf2py double :: a(n),b(n),x(n),y(m)
cf2py double :: k(m,n),cnx(n),incr_x(n),sei(m,m)    
        implicit none
        integer :: n,m,i  
        real*8 :: a(n),b(n),x(n),y(m),k(m,n),cnx(n)
        real*8 :: sei(m,m),sri(n,n),sr(n,n),incr_x(n)
        ! - - - local variables - - -
        real*8 :: kt(n,m), kt_sei(n,m),kt_sei_y(n,1)
        real*8 :: nx(n),inc_x(n,1)
        kt=transpose(k)
        call dot(kt,sei,kt_sei,n,m,m)
        call dot(kt_sei,k,sri,n,m,n)
        call inverse(sri,sr,n)
        call dot(kt_sei, y,kt_sei_y,n,m,1)
        call dot(sr,kt_sei_y,inc_x,n,n,1)
        do i=1,n
            incr_x(i)=inc_x(i,1)
            nx(i)=x(i)-inc_x(i,1)
        enddo
        call clipper(a,b,nx,cnx,n)
      end
      subroutine newton_se_gain_aver_cost(x, y, k, sei, sr 
     %           , gain, aver, cost,n,m)
cf2py intent(in) ::   x, y, k ,sei,sr
cf2py intent(out) :: gain, aver, cost 
cf2py intent(hide) :: n,m 
cf2py integer :: n,m
cf2py double :: x(n),y(m),k(m,n),sei(m,m),sr(n,n)  
cf2py double :: gain(n,m), aver(n,n),cost(1,1)
        implicit none
        integer :: n,m,i,j  
        real*8 :: x(n),y(m),k(m,n),kt(n,m),sei(m,m)
        real*8 :: gain(n,m),aver(n,n),sr(n,n)
        real*8 :: cost(1,1),yt(1,m),y1(m,1)
        real*8 :: seiy(m,1),kt_sei(n,m)
        kt=transpose(k)
        call dot(kt,sei,kt_sei,n,m,m)
        call dot(sr,kt_sei,gain,n,n,m)
        do i=1,n
            do j=1,n
                aver(i,j)=0.d0
            enddo
            aver(i,i)=1.d0
        enddo
        do i=1,m
             yt(1,i)=y(i)
             y1(i,1)=y(i)
        enddo
        call dot(sei,y1,seiy,m,m,1)
        call dot(yt,seiy,cost,1,m,1)
        
      end
      subroutine  newton_se_ret_err_cov(k,sei,sr,n,m)
cf2py intent(in) ::   y, k ,sei
cf2py intent(out) ::  sr 
cf2py intent(hide) :: n,m 
cf2py integer :: n,m
cf2py double :: k(m,n),sei(m,m),sr(n,n)  
        implicit none
        integer :: n,m 
        real*8 :: k(m,n),kt(n,m),sei(m,m)
        real*8 :: kt_sei(n,m),sri(n,n),sr(n,n)
        kt=transpose(k)
        call dot(kt,sei,kt_sei,n,m,m)
        call dot(kt_sei,k,sri,n,m,n)
        call inverse(sri,sr,n)
      end

! #######################################################################
! #######################################################################
! #######################################################################
! #######################################################################
! ###Optimal estimation with Gauss Newton 
      subroutine optimal_estimation_gauss_newton_operator
     %       (a, b, x, y, k, sei, sai,xa
     %        , cnx, incr_x,sri,sr,n,m)  
cf2py intent(in) :: a,b,x,y,k,sei,sai,xa
cf2py intent(out) :: cnx,incr_x,sri,sr
cf2py intent(hide) :: n,m 
cf2py integer :: n,m
cf2py double :: a(n),b(n),x(n),y(m),sai(n,n),xa(n)
cf2py double :: k(m,n),cnx(n),incr_x(n),sei(m,m)    
        implicit none
        integer :: n,m,i,j
        real*8 :: a(n),b(n),x(n),y(m),k(m,n),cnx(n),sai(n,n)
        real*8 :: sei(m,m),sri(n,n),sr(n,n),incr_x(n),xa(n)
        ! - - - local variables - - -
        real*8 :: kt(n,m), kt_sei(n,m),kt_sei_y(n,1)
        real*8 :: nx(n),inc_x(n,1),kt_sei_k(n,n),sai_dx(n,1)
        real*8 :: kt_sei_y_m_sai_dx(n,1),xamx(n)

        kt=transpose(k)
        call dot(kt,sei,kt_sei,n,m,m)
        call dot(kt_sei,k,kt_sei_k,n,m,n)
        do i=1,n
            do j=1,n
                sri(i,j)=kt_sei_k(i,j)+sai(i,j)        
            enddo
            xamx(i)=xa(i)-x(i)
        enddo        
        call inverse(sri,sr,n)       
        call dot(kt_sei, y,kt_sei_y,n,m,1)
        call dot(sai,xamx,sai_dx,n,n,1)
        do i=1,n
            kt_sei_y_m_sai_dx(i,1)=kt_sei_y(i,1)-sai_dx(i,1)
        enddo        
        call dot(sr,kt_sei_y_m_sai_dx,inc_x,n,n,1)
        
        do i=1,n
            incr_x(i)=inc_x(i,1)
            nx(i)=x(i)-inc_x(i,1)
        enddo
        call clipper(a,b,nx,cnx,n)
      end
        
      subroutine oe_gain_aver_cost(x, y, k, xa, sei, sai, sr 
     %           , gain, aver, cost,n,m)
cf2py intent(in) ::   x, y, k ,sei,sai,sr
cf2py intent(out) :: gain, aver, cost 
cf2py intent(hide) :: n,m 
cf2py integer :: n,m
cf2py double :: x(n),xa(n),y(m),k(m,n),sei(m,m),sai(n,n),sr(n,n)  
cf2py double :: gain(n,m), aver(n,n),cost(1,1)
        implicit none
        integer :: n,m,i
        real*8 :: x(n),y(m),xa(n)
        real*8 :: k(m,n),kt(n,m),sei(m,m),sai(n,n)
        real*8 :: gain(n,m),aver(n,n),sr(n,n)
        real*8 :: yt(1,m),y1(m,1),xamx1(n,1),xamxt(1,n)
        real*8 :: costy(1,1),costa(1,1),cost(1,1)
        real*8 :: seiy(m,1),kt_sei(n,m),saix(n,1)
        kt=transpose(k)
        do i=1,n
            xamx1(i,1)=xa(i)-x(i)
            xamxt(1,i)=xamx1(i,1)
        enddo        

        call dot(kt,sei,kt_sei,n,m,m)
        call dot(sr,kt_sei,gain,n,n,m)
        call dot(gain,k,aver,n,m,n)

        
        do i=1,m
             yt(1,i)=y(i)
             y1(i,1)=y(i)
        enddo
        call dot(sei,y1,seiy,m,m,1)
        call dot(yt,seiy,costy,1,m,1)
        call dot(sai,xamx1,saix,n,n,1)
        call dot(xamxt,saix,costa,1,m,1)
        cost(1,1)=costa(1,1)+costy(1,1)
       
      end
        
      subroutine  oe_ret_err_cov(k,sei,sai,sr,n,m)
cf2py intent(in) ::   y, k ,sei,sai
cf2py intent(out) ::  sr 
cf2py intent(hide) :: n,m 
cf2py integer :: n,m
cf2py double :: k(m,n),sei(m,m),sai(n,n),sr(n,n)  
        implicit none
        integer :: n,m,i,j 
        real*8 :: k(m,n),kt(n,m),sei(m,m),sai(n,n)
        real*8 :: kt_sei(n,m),kt_sei_k(n,n),sri(n,n),sr(n,n)
        kt=transpose(k)
        call dot(kt,sei,kt_sei,n,m,m)
        call dot(kt_sei,k,kt_sei_k,n,m,n)
        do i=1,n
            do j=1,n
                sri(i,j)=kt_sei_k(i,j)+sai(i,j)        
            enddo
        enddo        
        call inverse(sri,sr,n)
      end
        
        

 
